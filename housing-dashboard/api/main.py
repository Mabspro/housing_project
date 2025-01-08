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

app = FastAPI(title="Housing Market Analysis API", root_path="/api")

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

@app.get("/city-trends")
async def get_city_trends():
    try:
        logger.info("Attempting to fetch city trends data...")
        engine = get_db_connection()
        # Fetch the data
        query = text("""
            SELECT
                TO_CHAR(date, 'YYYY-MM') as date,
                AVG(CASE WHEN region_name = 'New York' THEN rental_price END) as "New York",
                AVG(CASE WHEN region_name = 'Los Angeles' THEN rental_price END) as "Los Angeles",
                AVG(CASE WHEN region_name = 'Chicago' THEN rental_price END) as "Chicago",
                AVG(CASE WHEN region_name = 'Dallas' THEN rental_price END) as "Dallas",
                AVG(CASE WHEN region_name = 'Miami' THEN rental_price END) as "Miami"
            FROM 
                rental_data
            GROUP BY
                date
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

@app.get("/growth-rates")
async def get_growth_rates():
    try:
        logger.info("Fetching growth rates data...")
        engine = get_db_connection()
        # Execute the main query
        query_str = """
            WITH monthly_data AS (
                SELECT 
                    date_trunc('month', date) as month_date,
                    MAX(CASE WHEN region_name = 'New York' THEN rental_yoy END) as "New York_YoY",
                    MAX(CASE WHEN region_name = 'Los Angeles' THEN rental_yoy END) as "Los Angeles_YoY",
                    MAX(CASE WHEN region_name = 'Chicago' THEN rental_yoy END) as "Chicago_YoY",
                    MAX(CASE WHEN region_name = 'Dallas' THEN rental_yoy END) as "Dallas_YoY",
                    MAX(CASE WHEN region_name = 'Miami' THEN rental_yoy END) as "Miami_YoY"
                FROM 
                    rental_data
                WHERE
                    region_name IN ('New York', 'Los Angeles', 'Chicago', 'Dallas', 'Miami')
                GROUP BY 
                    date_trunc('month', date)
            )
            SELECT
                TO_CHAR(month_date, 'YYYY-MM') AS formatted_date,
                ROUND(CAST("New York_YoY" AS numeric), 4) AS "New York_YoY",
                ROUND(CAST("Los Angeles_YoY" AS numeric), 4) AS "Los Angeles_YoY",
                ROUND(CAST("Chicago_YoY" AS numeric), 4) AS "Chicago_YoY",
                ROUND(CAST("Dallas_YoY" AS numeric), 4) AS "Dallas_YoY",
                ROUND(CAST("Miami_YoY" AS numeric), 4) AS "Miami_YoY"
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
                        round(float(val), 4) if pd.notna(val) else None 
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

@app.get("/market-heatmap")
async def get_market_heatmap():
    try:
        logger.info("Fetching market heatmap data...")
        engine = get_db_connection()
        query = text("""
            SELECT 
                TO_CHAR(date, 'YYYY-MM') as date,
                MAX(CASE WHEN region_name = 'New York' THEN rental_yoy END) as "New York_YoY",
                MAX(CASE WHEN region_name = 'Los Angeles' THEN rental_yoy END) as "Los Angeles_YoY",
                MAX(CASE WHEN region_name = 'Chicago' THEN rental_yoy END) as "Chicago_YoY",
                MAX(CASE WHEN region_name = 'Dallas' THEN rental_yoy END) as "Dallas_YoY",
                MAX(CASE WHEN region_name = 'Miami' THEN rental_yoy END) as "Miami_YoY"
            FROM 
                rental_data
            WHERE
                date = (SELECT MAX(date) FROM rental_data)
            GROUP BY 
                date;
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
