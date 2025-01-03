from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from typing import Dict, List
from datetime import datetime
import numpy as np
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Housing Market Analysis API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mabspro.github.io",  # Frontend hosted on GitHub Pages
        "http://localhost:3000",  # Local frontend for development
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    from urllib.parse import quote_plus
    password = quote_plus(os.getenv('DB_PASSWORD'))
    db_url = f"postgresql://{os.getenv('DB_USER')}:{password}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(db_url)

@app.get("/api/city-trends")
async def get_city_trends():
    try:
        logger.info("Attempting to fetch city trends data...")
        engine = get_db_connection()
        # First, get the data types of columns
        info_query = text("""
            SELECT 
                column_name,
                data_type 
            FROM 
                information_schema.columns 
            WHERE 
                table_name = 'housing_prices_cleaned';
        """)
        logger.debug(f"Executing schema query: {info_query}")
        with engine.connect() as conn:
            result = conn.execute(info_query)
            columns = [(row[0], row[1]) for row in result]
            logger.debug(f"Schema columns: {columns}")

        # Then fetch the data
        query = text("""
            SELECT
                TO_CHAR(date, 'YYYY-MM') as date,
                "U.S. National",
                "NY-New York",
                "CA-Los Angeles",
                "IL-Chicago",
                "TX-Dallas",
                "FL-Miami"
            FROM 
                housing_prices_cleaned
            ORDER BY 
                date;
        """)
        logger.debug(f"Executing data query: {query}")
        df = pd.read_sql(query, engine)
        logger.info(f"Query executed successfully. Row count: {len(df)}")
        logger.debug(f"DataFrame head: \n{df.head()}")

        # Create the response structure
        # Validate data before creating response
        if len(df) == 0:
            raise HTTPException(status_code=404, detail="No data found")
            
        # Convert DataFrame to records format first
        records = df.to_dict(orient='records')
        
        # Then structure the response
        response = {
            "date": [record['date'] for record in records],
            "values": {
                col: [float(record[col]) if pd.notna(record[col]) else None 
                     for record in records]
                for col in df.columns if col != 'date'
            },
            "timestamp": datetime.now().isoformat()
        }
        return response
    except Exception as e:
        error_msg = f"Error fetching city trends: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/growth-rates")
async def get_growth_rates():
    try:
        logger.info("Fetching growth rates data...")
        engine = get_db_connection()
        # First check the table schema
        info_query = text("""
            SELECT 
                column_name,
                data_type 
            FROM 
                information_schema.columns 
            WHERE 
                table_name = 'housing_prices_cleaned';
        """)
        logger.debug(f"Executing schema query: {info_query}")
        with engine.connect() as conn:
            result = conn.execute(info_query)
            columns = [(row[0], row[1]) for row in result]
            logger.debug(f"Schema columns: {columns}")

        # Then execute the main query
        query_str = """
            WITH monthly_data AS (
                SELECT 
                    date_trunc('month', date) as month_date,
                    AVG("NY-New York_YoY") as "NY-New York_YoY",
                    AVG("CA-Los Angeles_YoY") as "CA-Los Angeles_YoY",
                    AVG("IL-Chicago_YoY") as "IL-Chicago_YoY",
                    AVG("TX-Dallas_YoY") as "TX-Dallas_YoY",
                    AVG("FL-Miami_YoY") as "FL-Miami_YoY"
                FROM 
                    housing_prices_cleaned
                GROUP BY 
                    date_trunc('month', date)
            )
            SELECT
                TO_CHAR(month_date, 'YYYY-MM') AS formatted_date,
                ROUND("NY-New York_YoY"::numeric, 2) AS "NY-New York_YoY",
                ROUND("CA-Los Angeles_YoY"::numeric, 2) AS "CA-Los Angeles_YoY",
                ROUND("IL-Chicago_YoY"::numeric, 2) AS "IL-Chicago_YoY",
                ROUND("TX-Dallas_YoY"::numeric, 2) AS "TX-Dallas_YoY",
                ROUND("FL-Miami_YoY"::numeric, 2) AS "FL-Miami_YoY"
            FROM 
                monthly_data
            ORDER BY 
                month_date;
        """
        # Print raw query for debugging
        print("\nExecuting query:")
        print(query_str)
        logger.info(f"Raw query being executed: {query_str}")
        
        query = text(query_str)
        logger.debug(f"Executing growth rates query: {query}")
        try:
            df = pd.read_sql(query, engine)
            logger.info("Query executed successfully")
            logger.debug(f"DataFrame columns: {df.columns.tolist()}")
            logger.debug(f"DataFrame shape: {df.shape}")
            logger.debug(f"First row: {df.iloc[0].to_dict() if len(df) > 0 else 'No data'}")
            # Convert DataFrame to records format first
            records = df.to_dict(orient='records')
            
            # Then structure the response
            # Ensure proper date formatting and data structure
            response = {
                "date": df['formatted_date'].tolist(),  # Use pandas tolist() for proper serialization
                "values": {
                    col.replace('_YoY', ''): [
                        round(float(val), 2) if pd.notna(val) else None 
                        for val in df[col]
                    ]
                    for col in df.columns if col != 'formatted_date'
                },
                "metadata": {
                    "total_records": len(df),
                    "timestamp": datetime.now().isoformat()
                }
            }
            logger.debug(f"Response structure: {response.keys()}")
            logger.debug(f"Sample dates: {response['date'][:5]}")
            return response
        except pd.io.sql.DatabaseError as db_error:
            error_msg = f"Database query error: {str(db_error)}"
            logger.error(error_msg, exc_info=True)
            raise HTTPException(status_code=500, detail=error_msg)
        except ValueError as val_error:
            error_msg = f"Data validation error: {str(val_error)}"
            logger.error(error_msg, exc_info=True)
            raise HTTPException(status_code=422, detail=error_msg)
    except Exception as e:
        import traceback
        error_msg = f"Error fetching growth rates: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/market-heatmap")
async def get_market_heatmap():
    try:
        logger.info("Fetching market heatmap data...")
        engine = get_db_connection()
        query = text("""
            SELECT 
                TO_CHAR(date, 'YYYY-MM') as date,
                AVG("NY-New York_YoY") as "NY-New York_YoY",
                AVG("CA-Los Angeles_YoY") as "CA-Los Angeles_YoY",
                AVG("IL-Chicago_YoY") as "IL-Chicago_YoY",
                AVG("TX-Dallas_YoY") as "TX-Dallas_YoY",
                AVG("FL-Miami_YoY") as "FL-Miami_YoY"
            FROM 
                housing_prices_cleaned
            GROUP BY 
                date
            ORDER BY 
                date DESC
            LIMIT 1;
        """)
        logger.debug(f"Executing market heatmap query: {query}")
        df = pd.read_sql(query, engine)
        if len(df) == 0:
            logger.warning("No market heatmap data found")
            raise HTTPException(status_code=404, detail="No market heatmap data found")
        logger.info(f"Market heatmap query executed successfully. Row count: {len(df)}")
        logger.debug(f"DataFrame content: \n{df}")
        # Get markets and their growth rates
        # Convert DataFrame to records and get the first (and only) record
        record = df.to_dict(orient='records')[0]
        
        # Process the market rates
        market_rates = {
            col.replace('_YoY', ''): float(val) if pd.notna(val) else None
            for col, val in record.items() 
            if col.endswith('_YoY')
        }
        
        # Sort markets by growth rate
        sorted_markets = sorted(
            market_rates.items(), 
            key=lambda x: float('-inf') if x[1] is None else x[1], 
            reverse=True
        )
        
        response = {
            "markets": [market for market, _ in sorted_markets],
            "growthRates": [rate for _, rate in sorted_markets],
            "timestamp": datetime.now().isoformat()
        }
        logger.debug(f"Market heatmap API response: {response}")
        return response
    except Exception as e:
        error_msg = f"Error fetching market heatmap: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
