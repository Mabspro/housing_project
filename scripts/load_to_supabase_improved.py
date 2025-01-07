import os
import time
import logging
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import pandas as pd
import io

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('supabase_load.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Get database connection with retry mechanism"""
    env_path = Path(__file__).parent.parent / 'housing-dashboard/api/.env.production'
    if not env_path.exists():
        raise FileNotFoundError(f"Environment file not found at {env_path}")
        
    # Force clear any existing env vars
    for key in ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']:
        if key in os.environ:
            del os.environ[key]
            
    # Load fresh env vars
    load_dotenv(env_path, override=True)
    
    # Get and validate database parameters
    required_params = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    env_vars = {}
    for param in required_params:
        value = os.getenv(param)
        if not value:
            raise ValueError(f"Missing required environment variable: {param}")
        env_vars[param] = value
    
    # Log connection details (excluding sensitive info)
    logger.info(f"Connecting to Supabase database at {env_vars['DB_HOST']}")
    
    # Build connection parameters
    db_params = {
        'dbname': env_vars['DB_NAME'],
        'user': env_vars['DB_USER'],
        'password': env_vars['DB_PASSWORD'],
        'host': env_vars['DB_HOST'],
        'port': env_vars['DB_PORT'],
        'sslmode': 'require'  # Required for Supabase
    }
    
    retries = 3
    for attempt in range(retries):
        try:
            return psycopg2.connect(
                **db_params,
                connect_timeout=30,
                keepalives=1,
                keepalives_idle=30
            )
        except psycopg2.OperationalError as e:
            if attempt == retries - 1:
                logger.error(f"Failed to connect after {retries} attempts: {str(e)}")
                raise
            logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")
            time.sleep(5)

def validate_decimal_precision(df, column, precision, scale):
    """Validate decimal values against schema precision/scale"""
    max_value = 10 ** (precision - scale) - 1
    min_value = -max_value
    invalid_rows = df[
        (df[column].notna()) & 
        ((df[column] > max_value) | (df[column] < min_value))
    ]
    if not invalid_rows.empty:
        raise ValueError(f"Values in {column} exceed precision {precision},{scale}")

def validate_data(df, table_name):
    """Validate dataframe against table schema constraints"""
    schema_constraints = {
        'bls_housing_cpi': {
            'housing_cpi': (10, 2),
            'shelter_cpi': (10, 2),
            'fuels_utilities_cpi': (10, 2),
            'household_furnishings_cpi': (10, 2),
            'housing_cpi_mom': (6, 3),
            'shelter_cpi_mom': (6, 3),
            'fuels_utilities_mom': (6, 3),
            'furnishings_mom': (6, 3),
            'housing_cpi_yoy': (6, 3),
            'shelter_cpi_yoy': (6, 3),
            'fuels_utilities_yoy': (6, 3),
            'furnishings_yoy': (6, 3)
        },
        'census_housing': {
            'median_home_value': (12, 2),
            'median_monthly_cost': (8, 2),
            'vacancy_rate': (5, 2),
            'homeownership_rate': (5, 2)
        },
        'kaggle_housing_prices': {
            'us_national': (10, 2),
            'city_composite_20': (10, 2),
            'city_composite_10': (10, 2),
            'us_national_mom': (6, 3),
            'city_20_mom': (6, 3),
            'city_10_mom': (6, 3),
            'us_national_yoy': (6, 3),
            'city_20_yoy': (6, 3),
            'city_10_yoy': (6, 3)
        },
        'wages_education': {
            'wage_value': (10, 2),
            'wage_yoy_change': (6, 3)
        },
        'interest_rates': {
            'fed_funds_target': (5, 2),
            'fed_funds_upper': (5, 2),
            'fed_funds_lower': (5, 2),
            'effective_rate': (5, 2),
            'real_gdp_change': (5, 2),
            'unemployment_rate': (5, 2),
            'inflation_rate': (5, 2),
            'target_rate_mom': (6, 3),
            'effective_rate_mom': (6, 3),
            'target_rate_yoy': (6, 3),
            'effective_rate_yoy': (6, 3)
        },
        'zillow_housing': {
            'price': (12, 2),
            'price_mom': (6, 3),
            'price_yoy': (6, 3)
        },
        'zillow_home_value_index': {
            'home_value_index': (12, 2),
            'hvi_mom': (6, 3),
            'hvi_yoy': (6, 3)
        }
    }
    
    if table_name in schema_constraints:
        for column, (precision, scale) in schema_constraints[table_name].items():
            if column in df.columns:
                try:
                    validate_decimal_precision(df, column, precision, scale)
                except ValueError as e:
                    logger.error(f"Validation error in {table_name}.{column}: {str(e)}")
                    raise

def upsert_data(conn, df, table_name, unique_columns):
    """Upsert data directly using ON CONFLICT"""
    try:
        # Convert DataFrame to list of tuples
        data = df.values.tolist()
        
        # Get column names excluding id and created_at
        columns = [col for col in df.columns]
        columns_str = ', '.join([f'"{col}"' for col in columns])
        
        # Build the ON CONFLICT clause
        unique_cols_str = ', '.join([f'"{col}"' for col in unique_columns])
        update_cols = [col for col in columns if col not in unique_columns]
        update_str = ', '.join([f'"{col}" = EXCLUDED."{col}"' for col in update_cols])
        
        # Build the INSERT statement
        query = f"""
            INSERT INTO public.{table_name} ({columns_str})
            VALUES %s
            ON CONFLICT ({unique_cols_str})
            DO UPDATE SET {update_str}
        """
        
        # Execute the upsert
        with conn.cursor() as cur:
            execute_values(cur, query, data, template=None, page_size=100)
            conn.commit()
            
    except Exception as e:
        logger.error(f"Error in upsert process for {table_name}: {str(e)}")
        raise

def load_dataset(conn, dataset_name, df, table_name, unique_columns):
    """Load a single dataset with validation and error handling"""
    logger.info(f"Loading {dataset_name}...")
    try:
        validate_data(df, table_name)
        logger.info(f"Validated {len(df)} rows for {dataset_name}")
        
        upsert_data(conn, df, table_name, unique_columns)
        logger.info(f"Successfully loaded {dataset_name}")
        
    except psycopg2.Error as e:
        logger.error(f"Database error loading {dataset_name}: {str(e)}")
        raise
    except ValueError as e:
        logger.error(f"Validation error in {dataset_name}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading {dataset_name}: {str(e)}")
        raise

def check_existing_tables(conn):
    """Check existing tables and their structure in Supabase"""
    logger.info("Checking existing database structure...")
    
    with conn.cursor() as cur:
        # Check existing tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        existing_tables = [row[0] for row in cur.fetchall()]
        logger.info("\nExisting tables:")
        for table in existing_tables:
            # Get row count
            cur.execute(f"SELECT COUNT(*) FROM public.{table}")
            count = cur.fetchone()[0]
            
            # Get table structure
            cur.execute(f"""
                SELECT column_name, data_type, character_maximum_length, 
                       numeric_precision, numeric_scale
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = '{table}'
            """)
            columns = cur.fetchall()
            
            logger.info(f"\n{table}: {count} rows")
            logger.info("Columns:")
            for col in columns:
                logger.info(f"  {col[0]}: {col[1]}" + 
                          (f"({col[2]})" if col[2] else "") +
                          (f"({col[3]},{col[4]})" if col[3] else ""))

def load_data_to_supabase():
    """Main function to load all datasets to Supabase"""
    logger.info("Starting Supabase data loading process...")
    
    conn = None
    try:
        conn = get_db_connection()
        
        # First check existing database structure
        check_existing_tables(conn)
        
        # Ask user if they want to proceed with data loading
        logger.info("\nDatabase structure check complete.")
        
        # Load BLS data
        df = pd.read_csv('data/bls/bls_housing_processed.csv')
        # Select only the columns we need and map them to schema names
        df = df[['date', 'Fuels_Utilities', 'Household_Furnishings', 'Housing', 'Shelter']]
        column_mapping = {
            'date': 'date',
            'Fuels_Utilities': 'fuels_utilities_cpi',
            'Household_Furnishings': 'household_furnishings_cpi',
            'Housing': 'housing_cpi',
            'Shelter': 'shelter_cpi'
        }
        df = df.rename(columns=column_mapping)
        df['housing_cpi_mom'] = df['housing_cpi'].pct_change().round(3)
        df['shelter_cpi_mom'] = df['shelter_cpi'].pct_change().round(3)
        df['fuels_utilities_mom'] = df['fuels_utilities_cpi'].pct_change().round(3)
        df['furnishings_mom'] = df['household_furnishings_cpi'].pct_change().round(3)
        df['housing_cpi_yoy'] = df['housing_cpi'].pct_change(12).round(3)
        df['shelter_cpi_yoy'] = df['shelter_cpi'].pct_change(12).round(3)
        df['fuels_utilities_yoy'] = df['fuels_utilities_cpi'].pct_change(12).round(3)
        df['furnishings_yoy'] = df['household_furnishings_cpi'].pct_change(12).round(3)
        load_dataset(conn, "BLS Housing CPI", df, 'bls_housing_cpi', ['date'])
        
        # Load Census data
        df = pd.read_csv('data/census/census_housing_processed.csv')
        column_mapping = {
            'state': 'state',
            'year': 'year',
            'Total_Housing_Units': 'total_housing_units',
            'Occupied_Units': 'occupied_units',
            'Vacant_Units': 'vacant_units',
            'Owner_Occupied': 'owner_occupied',
            'Renter_Occupied': 'renter_occupied',
            'Median_Home_Value': 'median_home_value',
            'Median_Monthly_Housing_Cost': 'median_monthly_cost',
            'Vacancy_Rate': 'vacancy_rate',
            'Homeownership_Rate': 'homeownership_rate'
        }
        df = df.rename(columns=column_mapping)
        load_dataset(conn, "Census Housing", df, 'census_housing', ['state', 'year'])
        
        # Load Kaggle Housing Prices
        df = pd.read_csv('data/kaggle/housing/kaggle_housing_processed.csv')
        # Select only the columns we need
        df = df[['date', 'U.S. National', '20-City Composite', '10-City Composite']]
        column_mapping = {
            'date': 'date',
            'U.S. National': 'us_national',
            '20-City Composite': 'city_composite_20',
            '10-City Composite': 'city_composite_10'
        }
        df = df.rename(columns=column_mapping)
        df['us_national_mom'] = df['us_national'].pct_change().round(3)
        df['city_20_mom'] = df['city_composite_20'].pct_change().round(3)
        df['city_10_mom'] = df['city_composite_10'].pct_change().round(3)
        df['us_national_yoy'] = df['us_national'].pct_change(12).round(3)
        df['city_20_yoy'] = df['city_composite_20'].pct_change(12).round(3)
        df['city_10_yoy'] = df['city_composite_10'].pct_change(12).round(3)
        load_dataset(conn, "Kaggle Housing Prices", df, 'kaggle_housing_prices', ['date'])
        
        # Load Wages data
        df = pd.read_csv('data/kaggle/wages/kaggle_wages_processed.csv')
        melted_df = pd.melt(df, id_vars=['Year'], var_name='category', value_name='wage_value')
        melted_df[['demographic_group', 'education_level']] = melted_df['category'].str.split('_', n=1, expand=True)
        melted_df = melted_df.drop('category', axis=1)
        melted_df = melted_df.rename(columns={'Year': 'year'})
        melted_df['wage_yoy_change'] = melted_df.groupby(['demographic_group', 'education_level'])['wage_value'].pct_change(fill_method=None).round(3)
        melted_df['wage_yoy_change'] = melted_df['wage_yoy_change'].replace([float('inf'), float('-inf')], None)
        load_dataset(conn, "Wages Education", melted_df, 'wages_education', ['year', 'education_level', 'demographic_group'])
        
        # Load Interest Rates data
        df = pd.read_csv('data/kaggle/interest_rates/kaggle_interest_rates_processed.csv')
        # First rename columns
        column_mapping = {
            'Date': 'date',
            'Federal Funds Target Rate': 'fed_funds_target',
            'Federal Funds Upper Target': 'fed_funds_upper',
            'Federal Funds Lower Target': 'fed_funds_lower',
            'Effective Federal Funds Rate': 'effective_rate',
            'Real GDP (Percent Change)': 'real_gdp_change',
            'Unemployment Rate': 'unemployment_rate',
            'Inflation Rate': 'inflation_rate'
        }
        df = df.rename(columns=column_mapping)
        
        # Calculate rate changes
        df['target_rate_mom'] = df['fed_funds_target'].pct_change(fill_method=None).round(3)
        df['effective_rate_mom'] = df['effective_rate'].pct_change(fill_method=None).round(3)
        df['target_rate_yoy'] = df['fed_funds_target'].pct_change(12, fill_method=None).round(3)
        df['effective_rate_yoy'] = df['effective_rate'].pct_change(12, fill_method=None).round(3)
        
        # Replace inf values with None
        for col in ['target_rate_mom', 'effective_rate_mom', 'target_rate_yoy', 'effective_rate_yoy']:
            df[col] = df[col].replace([float('inf'), float('-inf')], None)
        
        # Ensure columns are in the correct order
        columns = [
            'date', 'fed_funds_target', 'fed_funds_upper', 'fed_funds_lower',
            'effective_rate', 'real_gdp_change', 'unemployment_rate', 'inflation_rate',
            'target_rate_mom', 'effective_rate_mom', 'target_rate_yoy', 'effective_rate_yoy'
        ]
        df = df[columns]
        load_dataset(conn, "Interest Rates", df, 'interest_rates', ['date'])
        
        # Load Zillow Housing data
        df = pd.read_csv('data/kaggle/zillow/kaggle_zillow_processed.csv')
        # Select only the columns we need
        df = df[['Date', 'RegionName', 'State', 'Metro', 'CountyName', 'Price', 'Price_MoM', 'Price_YoY']]
        column_mapping = {
            'Date': 'date',
            'RegionName': 'region_name',
            'State': 'state',
            'Metro': 'metro_area',
            'CountyName': 'county_name',
            'Price': 'price',
            'Price_MoM': 'price_mom',
            'Price_YoY': 'price_yoy'
        }
        df = df.rename(columns=column_mapping)
        # Ensure columns are in the correct order
        columns = ['date', 'region_name', 'state', 'metro_area', 'county_name', 'price', 'price_mom', 'price_yoy']
        df = df[columns]
        df = df.sort_values(['date', 'region_name']).drop_duplicates(['date', 'region_name'], keep='last')
        load_dataset(conn, "Zillow Housing", df, 'zillow_housing', ['date', 'region_name'])
        
        # Load Zillow HVI data
        df = pd.read_csv('data/cleaned/zillow_hvi_cleaned.csv')
        df['date'] = pd.to_datetime(df['date'])
        state_cols = [col for col in df.columns if col != 'date' and not col.endswith('_MoM')]
        df_melted = pd.melt(df, id_vars=['date'], value_vars=state_cols,
                           var_name='state', value_name='home_value_index')
        df_melted = df_melted.sort_values(['date', 'state']).drop_duplicates(['date', 'state'])
        df_melted['home_value_index'] = pd.to_numeric(df_melted['home_value_index'], errors='coerce')
        df_melted = df_melted.sort_values(['date', 'state', 'home_value_index'], ascending=[True, True, False])
        df_melted = df_melted.drop_duplicates(['date', 'state'], keep='first')
        
        dfs = []
        for state in df_melted['state'].unique():
            state_df = df_melted[df_melted['state'] == state].copy()
            state_df = state_df.sort_values('date')
            state_df['hvi_mom'] = state_df['home_value_index'].pct_change().round(3)
            state_df['hvi_yoy'] = state_df['home_value_index'].pct_change(12).round(3)
            dfs.append(state_df)
        df_melted = pd.concat(dfs, ignore_index=True)
        
        for col in ['hvi_mom', 'hvi_yoy']:
            df_melted[col] = df_melted[col].replace([float('inf'), float('-inf')], None)
        load_dataset(conn, "Zillow Home Value Index", df_melted, 'zillow_home_value_index', ['date', 'state'])
        
        # Verify all data was loaded
        with conn.cursor() as cur:
            tables = {
                'BLS Housing CPI': 'bls_housing_cpi',
                'Census Housing': 'census_housing',
                'Kaggle Housing Prices': 'kaggle_housing_prices',
                'Wages Education': 'wages_education',
                'Interest Rates': 'interest_rates',
                'Zillow Housing': 'zillow_housing',
                'Zillow Home Value Index': 'zillow_home_value_index'
            }
            logger.info("\nVerifying data loaded:")
            for name, table in tables.items():
                cur.execute(f"SELECT COUNT(*) FROM public.{table}")
                count = cur.fetchone()[0]
                logger.info(f"{name}: {count} rows")
        
        logger.info("\nAll data loaded and committed successfully!")
        
    except Exception as e:
        logger.error(f"Error in data loading process: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    try:
        load_data_to_supabase()
    except Exception as e:
        logger.error(f"Failed to complete data loading: {str(e)}")
        exit(1)
