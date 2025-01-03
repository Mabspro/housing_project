import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def extract_data():
    # Database connection
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    
    # Read data into DataFrame
    query = "SELECT * FROM housing_prices;"
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df

def validate_data(df):
    print("\nData Validation Report:")
    print("=======================")
    
    # Check for missing values
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    # Check data types
    print("\nData Types:")
    print(df.dtypes)
    
    # Basic statistics
    print("\nBasic Statistics:")
    print(df.describe())

if __name__ == "__main__":
    # Extract data
    print("Extracting data from PostgreSQL...")
    df = extract_data()
    
    # Validate data
    validate_data(df)
