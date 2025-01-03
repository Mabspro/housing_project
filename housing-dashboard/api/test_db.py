import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    try:
        from urllib.parse import quote_plus
        password = quote_plus(os.getenv('DB_PASSWORD'))
        db_url = f"postgresql://{os.getenv('DB_USER')}:{password}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            from sqlalchemy import text
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful:", result.fetchone())
            
            # Test if the housing_prices_cleaned table exists and has data
            result = connection.execute(text("SELECT COUNT(*) FROM housing_prices_cleaned"))
            count = result.fetchone()[0]
            print(f"Number of rows in housing_prices_cleaned: {count}")
            
            # Fetch and print column names
            columns_result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'housing_prices_cleaned'"))
            column_names = [row[0] for row in columns_result]
            print("Column names in housing_prices_cleaned:", column_names)
            
    except Exception as e:
        print("Database connection failed:", str(e))

if __name__ == "__main__":
    test_connection()
