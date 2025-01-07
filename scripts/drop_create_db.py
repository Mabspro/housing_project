import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path('scripts/scrapers/.env')
load_dotenv(env_path)

# Get connection parameters without database
conn_params = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Connect to default postgres database
conn_params['dbname'] = 'postgres'

try:
    # Connect to postgres database
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Terminate all connections to housing_db
    cur.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'housing_db'
        AND pid <> pg_backend_pid()
    """)
    
    # Now drop housing_db
    cur.execute("DROP DATABASE IF EXISTS housing_db")
    print("Dropped existing housing_db if it existed")
    
    # Create new housing_db
    cur.execute("CREATE DATABASE housing_db")
    print("Created new housing_db")
    
    cur.close()
    conn.close()
    print("Database operations completed successfully")
except Exception as e:
    print(f"Error: {str(e)}")
