import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

def get_db_connection():
    from urllib.parse import quote_plus
    password = quote_plus(os.getenv('DB_PASSWORD'))
    db_url = f"postgresql://{os.getenv('DB_USER')}:{password}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(db_url)

def main():
    try:
        print("Attempting to connect to database...")
        engine = get_db_connection()
        
        # Test connection
        with engine.connect() as conn:
            print("\nChecking tables...")
            # Check if zillow_housing table exists and has data
            result = conn.execute(text("""
                SELECT COUNT(*) as count, 
                       MIN(date) as min_date, 
                       MAX(date) as max_date,
                       COUNT(DISTINCT region_name) as regions
                FROM zillow_housing;
            """))
            row = result.fetchone()
            print(f"\nzillow_housing table stats:")
            print(f"Total rows: {row[0]}")
            print(f"Date range: {row[1]} to {row[2]}")
            print(f"Number of regions: {row[3]}")
            
            # Sample some actual data
            print("\nSample data from zillow_housing:")
            result = conn.execute(text("""
                SELECT date, region_name, price, price_yoy
                FROM zillow_housing
                LIMIT 5;
            """))
            for row in result:
                print(row)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
