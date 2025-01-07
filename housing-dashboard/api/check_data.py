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
        print("Checking database tables...")
        engine = get_db_connection()
        
        with engine.connect() as conn:
            # List all tables
            tables_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            result = conn.execute(tables_query)
            tables = result.fetchall()
            print("\nFound tables:")
            for table in tables:
                print(f"\n{table[0]}:")
                # Get row count for each table
                count_query = text(f"SELECT COUNT(*) FROM {table[0]};")
                count_result = conn.execute(count_query)
                count = count_result.fetchone()[0]
                print(f"  Row count: {count}")
        
        print("\nChecking zillow_housing data...")
        engine = get_db_connection()
        
        with engine.connect() as conn:
            # Check major cities
            cities_query = text("""
                SELECT DISTINCT region_name 
                FROM zillow_housing 
                WHERE LOWER(region_name) LIKE '%new york%'
                   OR LOWER(region_name) LIKE '%los angeles%'
                   OR LOWER(region_name) LIKE '%chicago%'
                   OR LOWER(region_name) LIKE '%dallas%'
                   OR LOWER(region_name) LIKE '%miami%'
                ORDER BY region_name;
            """)
            result = conn.execute(cities_query)
            cities = result.fetchall()
            print("\nFound cities:")
            for city in cities:
                print(city[0])
            
            # Check for non-null price data
            price_query = text("""
                SELECT region_name, COUNT(*) as total_rows,
                       COUNT(price) as rows_with_price,
                       COUNT(price_yoy) as rows_with_yoy,
                       MIN(date) as min_date,
                       MAX(date) as max_date
                FROM zillow_housing
                WHERE region_name IN ('NY-New York', 'CA-Los Angeles', 'IL-Chicago', 'TX-Dallas', 'FL-Miami')
                GROUP BY region_name
                ORDER BY region_name;
            """)
            result = conn.execute(price_query)
            print("\nPrice data statistics:")
            for row in result:
                print(f"\n{row[0]}:")
                print(f"  Total rows: {row[1]}")
                print(f"  Rows with price: {row[2]}")
                print(f"  Rows with YoY: {row[3]}")
                print(f"  Date range: {row[4]} to {row[5]}")
            
            # Get latest prices for each city
            sample_query = text("""
                SELECT 
                    region_name,
                    price,
                    date
                FROM zillow_housing
                WHERE region_name IN ('New York', 'Los Angeles', 'Chicago', 'Dallas', 'Miami')
                AND date = (SELECT MAX(date) FROM zillow_housing)
                ORDER BY region_name;
            """)
            result = conn.execute(sample_query)
            print("\nSample price data:")
            for row in result:
                print(f"{row[0]}: Price: ${row[1]:,.2f}, Date: {row[2]}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
