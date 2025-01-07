import os
from pathlib import Path
import subprocess
import psycopg2
from dotenv import load_dotenv
import sqlparse
import pandas as pd
import io

def get_db_connection():
    """Get database connection using Supabase credentials"""
    env_path = Path(__file__).parent.parent / 'housing-dashboard/api/.env.production'
    load_dotenv(env_path)
    
    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    
    return psycopg2.connect(**db_params)

def copy_from_stringio(conn, df, table_name, columns=None):
    """Efficiently load DataFrame to PostgreSQL using COPY"""
    columns = columns or df.columns.tolist()
    df_to_load = df[columns]
    output = io.StringIO()
    df_to_load.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    
    with conn.cursor() as cur:
        try:
            columns_str = ', '.join([f'"{col}"' for col in columns])
            cur.copy_expert(
                f"COPY public.{table_name} ({columns_str}) FROM STDIN WITH CSV DELIMITER E'\\t' NULL ''",
                output
            )
        except Exception as e:
            print(f"Error copying data to {table_name}: {str(e)}")
            raise

def load_schema_to_supabase():
    """Load schema.sql to Supabase database"""
    schema_path = Path(__file__).parent / 'supabase_schema.sql'
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("Creating tables in Supabase...")
        
        # Execute the entire schema as one statement
        try:
            cur.execute(schema_sql)
            conn.commit()
            print("Schema executed successfully.")
        except Exception as e:
            conn.rollback()
            error_message = f"Error executing schema: {str(e)}"
            print(error_message)
            raise Exception(error_message)
        
        print("\nSchema loaded successfully")
        cur.close()
    except Exception as e:
        print(f"Error loading schema: {str(e)}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def load_data_to_supabase():
    """Load data to Supabase using a single connection"""
    with get_db_connection() as conn:
        try:
            # Load BLS data
            print("\nLoading BLS data...")
            df = pd.read_csv('data/bls/bls_housing_processed.csv')
            column_mapping = {
                'date': 'date',
                'Fuels_Utilities': 'fuels_utilities_cpi',
                'Household_Furnishings': 'household_furnishings_cpi',
                'Housing': 'housing_cpi',
                'Housing_All': 'housing_all_cpi',
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
            columns = [
                'date', 'housing_cpi', 'shelter_cpi', 'fuels_utilities_cpi', 'household_furnishings_cpi',
                'housing_cpi_mom', 'shelter_cpi_mom', 'fuels_utilities_mom', 'furnishings_mom',
                'housing_cpi_yoy', 'shelter_cpi_yoy', 'fuels_utilities_yoy', 'furnishings_yoy'
            ]
            print(f"Loading {len(df)} rows...")
            copy_from_stringio(conn, df, 'bls_housing_cpi', columns)
            
            # Load Census data
            print("\nLoading Census data...")
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
            print(f"Loading {len(df)} rows...")
            copy_from_stringio(conn, df, 'census_housing', list(column_mapping.values()))
            
            # Load Kaggle Housing Prices
            print("\nLoading Kaggle Housing Prices...")
            df = pd.read_csv('data/kaggle/housing/kaggle_housing_processed.csv')
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
            columns = ['date', 'us_national', 'city_composite_20', 'city_composite_10',
                      'us_national_mom', 'city_20_mom', 'city_10_mom',
                      'us_national_yoy', 'city_20_yoy', 'city_10_yoy']
            print(f"Loading {len(df)} rows...")
            copy_from_stringio(conn, df, 'kaggle_housing_prices', columns)
            
            # Load Wages data
            print("\nLoading Wages data...")
            df = pd.read_csv('data/kaggle/wages/kaggle_wages_processed.csv')
            melted_df = pd.melt(df, id_vars=['Year'], var_name='category', value_name='wage_value')
            melted_df[['demographic_group', 'education_level']] = melted_df['category'].str.split('_', n=1, expand=True)
            melted_df = melted_df.drop('category', axis=1)
            melted_df = melted_df.rename(columns={'Year': 'year'})
            melted_df['wage_yoy_change'] = melted_df.groupby(['demographic_group', 'education_level'])['wage_value'].pct_change(fill_method=None).round(3)
            melted_df['wage_yoy_change'] = melted_df['wage_yoy_change'].replace([float('inf'), float('-inf')], None)
            columns = ['year', 'education_level', 'demographic_group', 'wage_value', 'wage_yoy_change']
            print(f"Loading {len(melted_df)} rows...")
            copy_from_stringio(conn, melted_df, 'wages_education', columns)
            
            # Load Interest Rates data
            print("\nLoading Interest Rates data...")
            df = pd.read_csv('data/kaggle/interest_rates/kaggle_interest_rates_processed.csv')
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
            df['target_rate_mom'] = df['fed_funds_target'].pct_change(fill_method=None).round(3)
            df['effective_rate_mom'] = df['effective_rate'].pct_change(fill_method=None).round(3)
            df['target_rate_yoy'] = df['fed_funds_target'].pct_change(12, fill_method=None).round(3)
            df['effective_rate_yoy'] = df['effective_rate'].pct_change(12, fill_method=None).round(3)
            for col in ['target_rate_mom', 'effective_rate_mom', 'target_rate_yoy', 'effective_rate_yoy']:
                df[col] = df[col].replace([float('inf'), float('-inf')], None)
            columns = ['date', 'fed_funds_target', 'fed_funds_upper', 'fed_funds_lower',
                      'effective_rate', 'real_gdp_change', 'unemployment_rate', 'inflation_rate',
                      'target_rate_mom', 'effective_rate_mom', 'target_rate_yoy', 'effective_rate_yoy']
            print(f"Loading {len(df)} rows...")
            copy_from_stringio(conn, df, 'interest_rates', columns)
            
            # Load Zillow Housing data
            print("\nLoading Zillow Housing data...")
            df = pd.read_csv('data/kaggle/zillow/kaggle_zillow_processed.csv')
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
            df = df.sort_values(['date', 'region_name']).drop_duplicates(['date', 'region_name'], keep='last')
            print(f"Loading {len(df)} rows...")
            copy_from_stringio(conn, df, 'zillow_housing', list(column_mapping.values()))
            
            # Load Zillow HVI data
            print("\nLoading Zillow HVI data...")
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
            columns = ['date', 'state', 'home_value_index', 'hvi_mom', 'hvi_yoy']
            print(f"Loading {len(df_melted)} rows...")
            copy_from_stringio(conn, df_melted, 'zillow_home_value_index', columns)
            
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
                print("\nVerifying data loaded:")
                for name, table in tables.items():
                    cur.execute(f"SELECT COUNT(*) FROM public.{table}")
                    count = cur.fetchone()[0]
                    print(f"{name}: {count} rows")
            
            conn.commit()
            print("\nAll data loaded and committed successfully!")
            
        except Exception as e:
            conn.rollback()
            print(f"Error loading data: {str(e)}")
            raise

if __name__ == "__main__":
    print("Starting Supabase data loading process...")
    load_schema_to_supabase()
    load_data_to_supabase()
    print("\nCompleted loading data to Supabase")
