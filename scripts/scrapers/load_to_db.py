import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from pathlib import Path
import io

class DatabaseLoader:
    def __init__(self):
        """Initialize database connection using environment variables"""
        # Load environment variables from the correct location
        env_path = Path(__file__).parent / '.env'
        load_dotenv(env_path)
        
        # Store connection parameters
        self.conn_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }

    def get_connection(self):
        """Create a new database connection"""
        return psycopg2.connect(**self.conn_params)

    def create_tables(self, drop_existing=True):
        """Create database tables from schema.sql"""
        schema_path = Path(__file__).parent / 'schema.sql'
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if drop_existing:
                        # Drop existing tables in reverse order to handle dependencies
                        print("\nDropping existing tables...")
                        tables = [
                            'zillow_home_value_index',
                            'zillow_housing',
                            'interest_rates',
                            'wages_education',
                            'kaggle_housing_prices',
                            'census_housing',
                            'bls_housing_cpi'
                        ]
                        for table in tables:
                            print(f"Dropping {table}...")
                            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                        conn.commit()
                    
                    # Create tables
                    print("\nCreating tables...")
                    cur.execute(schema_sql)
                    conn.commit()
                    print("\nDatabase tables created successfully")
                except Exception as e:
                    conn.rollback()
                    print(f"\nError creating tables: {str(e)}")
                    raise

    def copy_from_stringio(self, df, table_name, columns=None):
        """Efficiently load DataFrame to PostgreSQL using COPY"""
        # Use specified columns or all DataFrame columns
        columns = columns or df.columns.tolist()
        
        # Select only the specified columns
        df_to_load = df[columns]
        
        # Create string buffer
        output = io.StringIO()
        # Save df to string buffer
        df_to_load.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # Specify columns in COPY command
                    columns_str = ', '.join([f'"{col}"' for col in columns])
                    cur.copy_expert(
                        f"COPY {table_name} ({columns_str}) FROM STDIN WITH CSV DELIMITER E'\\t' NULL ''",
                        output
                    )
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"Error copying data to {table_name}: {str(e)}")
                    raise

    def load_bls_data(self):
        """Load BLS housing CPI data"""
        df = pd.read_csv('data/bls/bls_housing_processed.csv')
        
        # Rename columns to match schema
        column_mapping = {
            'date': 'date',
            'Fuels_Utilities': 'fuels_utilities_cpi',
            'Household_Furnishings': 'household_furnishings_cpi',
            'Housing': 'housing_cpi',
            'Housing_All': 'housing_all_cpi',
            'Shelter': 'shelter_cpi'
        }
        df = df.rename(columns=column_mapping)
        
        # Calculate MoM and YoY changes
        df['housing_cpi_mom'] = df['housing_cpi'].pct_change().round(3)
        df['shelter_cpi_mom'] = df['shelter_cpi'].pct_change().round(3)
        df['fuels_utilities_mom'] = df['fuels_utilities_cpi'].pct_change().round(3)
        df['furnishings_mom'] = df['household_furnishings_cpi'].pct_change().round(3)
        
        df['housing_cpi_yoy'] = df['housing_cpi'].pct_change(12).round(3)
        df['shelter_cpi_yoy'] = df['shelter_cpi'].pct_change(12).round(3)
        df['fuels_utilities_yoy'] = df['fuels_utilities_cpi'].pct_change(12).round(3)
        df['furnishings_yoy'] = df['household_furnishings_cpi'].pct_change(12).round(3)
        
        # Specify columns in the correct order to match schema
        columns = [
            'date',
            'housing_cpi', 'shelter_cpi', 'fuels_utilities_cpi', 'household_furnishings_cpi',
            'housing_cpi_mom', 'shelter_cpi_mom', 'fuels_utilities_mom', 'furnishings_mom',
            'housing_cpi_yoy', 'shelter_cpi_yoy', 'fuels_utilities_yoy', 'furnishings_yoy'
        ]
        
        self.copy_from_stringio(df, 'bls_housing_cpi', columns)
        print("BLS data loaded successfully")

    def load_census_data(self):
        """Load Census housing data"""
        df = pd.read_csv('data/census/census_housing_processed.csv')
        
        # Ensure column names match schema
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
        
        self.copy_from_stringio(df, 'census_housing', list(column_mapping.values()))
        print("Census data loaded successfully")

    def load_kaggle_housing_prices(self):
        """Load Kaggle housing prices data"""
        df = pd.read_csv('data/kaggle/housing/kaggle_housing_processed.csv')
        
        # Rename columns to match schema
        column_mapping = {
            'date': 'date',
            'U.S. National': 'us_national',
            '20-City Composite': 'city_composite_20',
            '10-City Composite': 'city_composite_10'
        }
        df = df.rename(columns=column_mapping)
        
        # Calculate MoM changes
        df['us_national_mom'] = df['us_national'].pct_change().round(3)
        df['city_20_mom'] = df['city_composite_20'].pct_change().round(3)
        df['city_10_mom'] = df['city_composite_10'].pct_change().round(3)
        
        # Calculate YoY changes
        df['us_national_yoy'] = df['us_national'].pct_change(12).round(3)
        df['city_20_yoy'] = df['city_composite_20'].pct_change(12).round(3)
        df['city_10_yoy'] = df['city_composite_10'].pct_change(12).round(3)
        
        # Specify columns in the correct order
        columns = ['date', 'us_national', 'city_composite_20', 'city_composite_10',
                  'us_national_mom', 'city_20_mom', 'city_10_mom',
                  'us_national_yoy', 'city_20_yoy', 'city_10_yoy']
        
        self.copy_from_stringio(df, 'kaggle_housing_prices', columns)
        print("Kaggle housing prices data loaded successfully")

    def load_wages_data(self):
        """Load wages by education data"""
        df = pd.read_csv('data/kaggle/wages/kaggle_wages_processed.csv')
        
        # Reshape data to match schema
        melted_df = pd.melt(
            df,
            id_vars=['Year'],
            var_name='category',
            value_name='wage_value'
        )
        
        # Split category into education_level and demographic_group
        melted_df[['demographic_group', 'education_level']] = melted_df['category'].str.split('_', n=1, expand=True)
        melted_df = melted_df.drop('category', axis=1)
        
        # Rename Year column to lowercase
        melted_df = melted_df.rename(columns={'Year': 'year'})
        
        # Calculate YoY changes and handle infinite values
        melted_df['wage_yoy_change'] = melted_df.groupby(['demographic_group', 'education_level'])['wage_value'].pct_change(fill_method=None).round(3)
        # Replace infinite values with None/NULL
        melted_df['wage_yoy_change'] = melted_df['wage_yoy_change'].replace([float('inf'), float('-inf')], None)
        
        # Specify columns in the correct order
        columns = ['year', 'education_level', 'demographic_group', 'wage_value', 'wage_yoy_change']
        
        self.copy_from_stringio(melted_df, 'wages_education', columns)
        print("Wages data loaded successfully")

    def load_interest_rates(self):
        """Load interest rates data"""
        df = pd.read_csv('data/kaggle/interest_rates/kaggle_interest_rates_processed.csv')
        
        # Ensure column names match schema
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
        
        # Calculate MoM and YoY changes with fill_method=None
        df['target_rate_mom'] = df['fed_funds_target'].pct_change(fill_method=None).round(3)
        df['effective_rate_mom'] = df['effective_rate'].pct_change(fill_method=None).round(3)
        df['target_rate_yoy'] = df['fed_funds_target'].pct_change(12, fill_method=None).round(3)
        df['effective_rate_yoy'] = df['effective_rate'].pct_change(12, fill_method=None).round(3)
        
        # Replace infinite values with None/NULL
        for col in ['target_rate_mom', 'effective_rate_mom', 'target_rate_yoy', 'effective_rate_yoy']:
            df[col] = df[col].replace([float('inf'), float('-inf')], None)
        
        # Specify columns in the correct order
        columns = ['date', 'fed_funds_target', 'fed_funds_upper', 'fed_funds_lower', 
                  'effective_rate', 'real_gdp_change', 'unemployment_rate', 'inflation_rate',
                  'target_rate_mom', 'effective_rate_mom', 'target_rate_yoy', 'effective_rate_yoy']
        
        self.copy_from_stringio(df, 'interest_rates', columns)
        print("Interest rates data loaded successfully")

    def load_zillow_data(self):
        """Load Zillow housing data"""
        df = pd.read_csv('data/kaggle/zillow/kaggle_zillow_processed.csv')
        
        # Ensure column names match schema
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
        
        # Sort by date and region_name, keep only the latest entry for each combination
        df = df.sort_values(['date', 'region_name']).drop_duplicates(['date', 'region_name'], keep='last')
        
        self.copy_from_stringio(df, 'zillow_housing', list(column_mapping.values()))
        print("Zillow housing data loaded successfully")

    def load_zillow_hvi(self):
        """Load Zillow Home Value Index data"""
        # Read from cleaned data instead of processed
        df = pd.read_csv('data/cleaned/zillow_hvi_cleaned.csv')
        
        # Ensure date is in datetime format
        df['date'] = pd.to_datetime(df['date'])
        
        # Get state columns (exclude date and any _MoM columns)
        state_cols = [col for col in df.columns if col != 'date' and not col.endswith('_MoM')]
        
        # Melt state columns into rows
        df_melted = pd.melt(
            df,
            id_vars=['date'],
            value_vars=state_cols,
            var_name='state',
            value_name='home_value_index'
        )
        
        # Sort by date and state, remove any duplicates
        df_melted = df_melted.sort_values(['date', 'state']).drop_duplicates(['date', 'state'])
        
        # Convert home_value_index to numeric and handle duplicates
        df_melted['home_value_index'] = pd.to_numeric(df_melted['home_value_index'], errors='coerce')
        
        # Sort by date and state, then remove duplicates keeping the latest value
        df_melted = df_melted.sort_values(['date', 'state', 'home_value_index'], ascending=[True, True, False])
        df_melted = df_melted.drop_duplicates(['date', 'state'], keep='first')
        
        # Calculate changes for each state separately to avoid cross-state calculations
        dfs = []
        for state in df_melted['state'].unique():
            state_df = df_melted[df_melted['state'] == state].copy()
            state_df = state_df.sort_values('date')
            
            # Calculate MoM and YoY changes
            state_df['hvi_mom'] = state_df['home_value_index'].pct_change().round(3)
            state_df['hvi_yoy'] = state_df['home_value_index'].pct_change(12).round(3)
            
            dfs.append(state_df)
        
        # Combine all states back together
        df_melted = pd.concat(dfs, ignore_index=True)
        
        # Replace infinite values with None/NULL
        for col in ['hvi_mom', 'hvi_yoy']:
            df_melted[col] = df_melted[col].replace([float('inf'), float('-inf')], None)
        
        # Specify columns in the correct order
        columns = ['date', 'state', 'home_value_index', 'hvi_mom', 'hvi_yoy']
        
        self.copy_from_stringio(df_melted, 'zillow_home_value_index', columns)
        print("Zillow HVI data loaded successfully")

    def load_all_data(self, drop_existing=True):
        """Create tables and load all datasets"""
        print("Starting database loading process...")
        
        # Create tables first
        self.create_tables(drop_existing=drop_existing)
        
        # Load each dataset
        try:
            self.load_bls_data()
            self.load_census_data()
            self.load_kaggle_housing_prices()
            self.load_wages_data()
            self.load_interest_rates()
            self.load_zillow_data()
            self.load_zillow_hvi()
            print("\nAll data loaded successfully!")
        except Exception as e:
            print(f"Error loading data: {str(e)}")

def main():
    loader = DatabaseLoader()
    loader.load_all_data(drop_existing=True)

if __name__ == "__main__":
    main()
