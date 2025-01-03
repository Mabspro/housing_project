import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Database connection
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

# Read CSV file
csv_path = os.path.join('data', '1', 's_p_housing_data.csv')
df = pd.read_csv(csv_path)

# Create table
table_name = 'housing_prices'
columns = ', '.join([f'"{col}" TEXT' for col in df.columns])

with conn.cursor() as cur:
    # Drop table if exists
    cur.execute(f'DROP TABLE IF EXISTS {table_name};')
    
    # Create table
    create_table_query = f'''
    CREATE TABLE {table_name} (
        {columns}
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

print(f"Successfully loaded data into {table_name} table")
conn.close()
