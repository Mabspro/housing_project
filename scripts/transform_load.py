import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def clean_transform_data(df):
    # Rename columns
    df = df.rename(columns={'Unnamed: 0': 'date'})
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'], format='%m-%d-%Y')
    
    # Convert numeric columns to float
    numeric_cols = df.columns[df.columns != 'date']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # Handle missing values (if any)
    df = df.fillna(method='ffill').fillna(method='bfill')
    
    # Calculate MoM and YoY changes
    for col in numeric_cols:
        df[f'{col}_MoM'] = df[col].pct_change()
        df[f'{col}_YoY'] = df[col].pct_change(12)
    
    # Normalize indices to January 2000 = 100
    base_date = pd.to_datetime('2000-01-01')
    base_values = df[df['date'] == base_date][numeric_cols]
    df[numeric_cols] = df[numeric_cols].div(base_values.values) * 100
    
    return df

def save_to_postgres(df):
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    
    # Create new table for cleaned data
    table_name = 'housing_prices_cleaned'
    with conn.cursor() as cur:
        cur.execute(f'DROP TABLE IF EXISTS {table_name};')
        
        # Create table with appropriate data types
        create_table_query = f'''
        CREATE TABLE {table_name} (
            date DATE PRIMARY KEY,
            {', '.join([f'"{col}" FLOAT' for col in df.columns if col != 'date'])}
        );
        '''
        cur.execute(create_table_query)
        
        # Insert data
        for _, row in df.iterrows():
            insert_query = f'''
            INSERT INTO {table_name} ({', '.join([f'"{col}"' for col in df.columns])})
            VALUES ({', '.join(['%s'] * len(df.columns))});
            '''
            cur.execute(insert_query, tuple(row))
        
        conn.commit()
    conn.close()

def save_to_csv(df):
    os.makedirs('data/cleaned', exist_ok=True)
    df.to_csv('data/cleaned/housing_prices_cleaned.csv', index=False)

if __name__ == "__main__":
    # Extract data
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scripts.extract import extract_data
    print("Extracting data...")
    df = extract_data()
    
    # Transform data
    print("Transforming data...")
    df_cleaned = clean_transform_data(df)
    
    # Load data
    print("Saving cleaned data to PostgreSQL...")
    save_to_postgres(df_cleaned)
    
    print("Saving cleaned data to CSV...")
    save_to_csv(df_cleaned)
    
    print("Data transformation and loading complete!")
