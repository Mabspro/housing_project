import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
import pandas as pd

def test_connection():
    """Test connection to Supabase database"""
    # Clear any existing environment variables
    for key in ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']:
        if key in os.environ:
            del os.environ[key]
    
    # Load Supabase credentials from production env
    env_path = Path(__file__).parent.parent / 'housing-dashboard/api/.env.production'
    if not env_path.exists():
        raise FileNotFoundError(f"Production environment file not found at {env_path}")
    
    print(f"\nLoading credentials from: {env_path}")
    load_dotenv(env_path, override=True)
    
    # Get and validate database parameters
    required_params = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    missing_params = [param for param in required_params if not os.getenv(param)]
    if missing_params:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_params)}")
    
    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    
    print("\nAttempting to connect with parameters:")
    for key, value in db_params.items():
        # Don't print the actual password
        if key == 'password':
            print(f"{key}: {'*' * len(value)}")
        else:
            print(f"{key}: {value}")
    
    try:
        # Try to connect
        print("\nConnecting to Supabase...")
        conn = psycopg2.connect(**db_params)
        
        # Get server version
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()[0]
        print(f"\nConnection successful!")
        print(f"PostgreSQL version: {version}")
        
        # Check current user, role, and permissions
        cur.execute("""
            SELECT 
                current_user,
                current_database(),
                ARRAY(
                    SELECT r.rolname
                    FROM pg_catalog.pg_roles r
                    JOIN pg_catalog.pg_auth_members m ON m.roleid = r.oid
                    JOIN pg_catalog.pg_roles u ON u.oid = m.member
                    WHERE u.rolname = current_user
                ) as roles,
                has_schema_privilege('public', 'create') as can_create_in_public,
                has_schema_privilege('public', 'usage') as can_use_public
        """)
        user_info = cur.fetchone()
        print(f"\nConnected as user: {user_info[0]}")
        print(f"Current database: {user_info[1]}")
        print(f"Roles: {user_info[2]}")
        print(f"Can create in public schema: {user_info[3]}")
        print(f"Can use public schema: {user_info[4]}")

        # Check row counts for all tables
        print("\nChecking row counts for all tables...")
        tables = [
            'bls_housing_cpi',
            'census_housing',
            'kaggle_housing_prices',
            'wages_education',
            'interest_rates',
            'zillow_housing',
            'zillow_home_value_index'
        ]
        
        for table in tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM public.{table}")
                count = cur.fetchone()[0]
                print(f"{table}: {count} rows")
                
                # Get sample data
                cur.execute(f"SELECT * FROM public.{table} LIMIT 1")
                columns = [desc[0] for desc in cur.description]
                sample = cur.fetchone()
                if sample:
                    print(f"Sample row columns: {columns}")
                    print(f"Sample row values: {sample}\n")
                else:
                    print("No data found in table\n")
                
            except Exception as e:
                print(f"Error checking {table}: {str(e)}\n")
        
        cur.close()
        conn.close()
        print("\nConnection closed successfully")
        
    except Exception as e:
        print(f"\nError connecting to database: {str(e)}")
        raise

if __name__ == "__main__":
    test_connection()
