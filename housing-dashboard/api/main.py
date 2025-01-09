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

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Housing Market Analysis API",
        "available_endpoints": {
            "dashboard": [
                "/api/city-trends",  # Historical data from kaggle_housing_prices
                "/api/growth-rates",  # Historical growth rates
                "/api/market-heatmap"  # Current market performance
            ],
            "market_analysis": [
                "/api/market-trends",  # Current data from zillow_housing
                "/api/market-growth",  # Current growth rates
                "/api/market-heatmap",  # Current market performance
                "/api/rental-trends",  # Alias for market-trends (backward compatibility)
                "/api/rental-growth",  # Alias for market-growth (backward compatibility)
                "/api/rental-heatmap"  # Alias for market-heatmap (backward compatibility)
            ]
        },
        "documentation": "/docs"
    }

@app.get("/api/city-trends")
async def get_city_trends():
    try:
        logger.info("Attempting to fetch historical city trends data...")
        engine = get_db_connection()
        query = text("""
            SELECT
                TO_CHAR(date, 'YYYY-MM') as date,
                us_national as "National",
                city_composite_20 as "Top 20 Cities",
                city_composite_10 as "Top 10 Cities"
            FROM 
                kaggle_housing_prices
            ORDER BY 
                date;
        """)
        logger.debug(f"Executing historical trends query: {query}")
        df = pd.read_sql(query, engine)
        logger.info(f"Query executed successfully. Row count: {len(df)}")
        logger.debug(f"DataFrame head: \n{df.head()}")

        if len(df) == 0:
            raise HTTPException(status_code=404, detail="No historical trends data found")
            
        records = df.to_dict(orient='records')
        
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
        error_msg = f"Error fetching historical trends: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/growth-rates")
async def get_growth_rates():
    try:
        logger.info("Fetching historical growth rates data...")
        engine = get_db_connection()
        query = text("""
            SELECT
                TO_CHAR(date, 'YYYY-MM') AS formatted_date,
                us_national_yoy as "National",
                city_20_yoy as "Top 20 Cities",
                city_10_yoy as "Top 10 Cities"
            FROM 
                kaggle_housing_prices
            ORDER BY 
                date;
        """)
        logger.debug(f"Executing historical growth rates query: {query}")
        df = pd.read_sql(query, engine)
        logger.info(f"Query executed successfully")
        logger.debug(f"DataFrame columns: {df.columns.tolist()}")
        logger.debug(f"DataFrame shape: {df.shape}")
        logger.debug(f"First row: {df.iloc[0].to_dict() if len(df) > 0 else 'No data'}")

        records = df.to_dict(orient='records')
        
        response = {
            "date": [record['formatted_date'] for record in records],
            "values": {
                col: [round(float(record[col]), 2) if pd.notna(record[col]) else None 
                     for record in records]
                for col in df.columns if col != 'formatted_date'
            },
            "timestamp": datetime.now().isoformat()
        }
        return response
    except Exception as e:
        error_msg = f"Error fetching historical growth rates: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/market-trends")
@app.get("/api/rental-trends")
async def get_market_trends():
    try:
        logger.info("Attempting to fetch current market trends data...")
        engine = get_db_connection()
        query = text("""
            SELECT
                TO_CHAR(date, 'YYYY-MM') as date,
                AVG(CASE WHEN region_name = 'New York' THEN price_mom * 100 END) as "New York",
                AVG(CASE WHEN region_name = 'Los Angeles' THEN price_mom * 100 END) as "Los Angeles",
                AVG(CASE WHEN region_name = 'Chicago' THEN price_mom * 100 END) as "Chicago",
                AVG(CASE WHEN region_name = 'Dallas' THEN price_mom * 100 END) as "Dallas",
                AVG(CASE WHEN region_name = 'Miami' THEN price_mom * 100 END) as "Miami"
            FROM 
                zillow_housing
            WHERE
                region_name IN ('New York', 'Los Angeles', 'Chicago', 'Dallas', 'Miami')
                AND price_mom IS NOT NULL
            GROUP BY
                date
            ORDER BY 
                date;
        """)
        logger.debug(f"Executing current market trends query: {query}")
        df = pd.read_sql(query, engine)
        logger.info(f"Query executed successfully. Row count: {len(df)}")
        logger.debug(f"DataFrame head: \n{df.head()}")

        if len(df) == 0:
            raise HTTPException(status_code=404, detail="No current market trends data found")
            
        records = df.to_dict(orient='records')
        
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
        error_msg = f"Error fetching current market trends: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/market-growth")
@app.get("/api/rental-growth")
async def get_market_growth():
    try:
        logger.info("Fetching current market growth rates data...")
        engine = get_db_connection()
        query = text("""
            WITH monthly_data AS (
                SELECT 
                    date_trunc('month', date) as month_date,
                    MAX(CASE WHEN region_name = 'New York' THEN price_yoy * 100 END) as "New York_YoY",
                    MAX(CASE WHEN region_name = 'Los Angeles' THEN price_yoy * 100 END) as "Los Angeles_YoY",
                    MAX(CASE WHEN region_name = 'Chicago' THEN price_yoy * 100 END) as "Chicago_YoY",
                    MAX(CASE WHEN region_name = 'Dallas' THEN price_yoy * 100 END) as "Dallas_YoY",
                    MAX(CASE WHEN region_name = 'Miami' THEN price_yoy * 100 END) as "Miami_YoY"
                FROM 
                    zillow_housing
                WHERE
                    region_name IN ('New York', 'Los Angeles', 'Chicago', 'Dallas', 'Miami')
                    AND price_yoy IS NOT NULL
                GROUP BY 
                    date_trunc('month', date)
            )
            SELECT
                TO_CHAR(month_date, 'YYYY-MM') AS formatted_date,
                ROUND(CAST("New York_YoY" AS numeric), 2) AS "New York_YoY",
                ROUND(CAST("Los Angeles_YoY" AS numeric), 2) AS "Los Angeles_YoY",
                ROUND(CAST("Chicago_YoY" AS numeric), 2) AS "Chicago_YoY",
                ROUND(CAST("Dallas_YoY" AS numeric), 2) AS "Dallas_YoY",
                ROUND(CAST("Miami_YoY" AS numeric), 2) AS "Miami_YoY"
            FROM 
                monthly_data
            ORDER BY 
                month_date;
        """)
        logger.debug(f"Executing current market growth rates query: {query}")
        df = pd.read_sql(query, engine)
        logger.info(f"Query executed successfully")
        logger.debug(f"DataFrame columns: {df.columns.tolist()}")
        logger.debug(f"DataFrame shape: {df.shape}")
        logger.debug(f"First row: {df.iloc[0].to_dict() if len(df) > 0 else 'No data'}")

        records = df.to_dict(orient='records')
        
        response = {
            "date": [record['formatted_date'] for record in records],
            "values": {
                col.replace('_YoY', ''): [
                    round(float(record[col]), 2) if pd.notna(record[col]) else None 
                    for record in records
                ]
                for col in df.columns if col != 'formatted_date'
            },
            "timestamp": datetime.now().isoformat()
        }
        return response
    except Exception as e:
        error_msg = f"Error fetching current market growth rates: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/market-heatmap")
@app.get("/api/rental-heatmap")
async def get_market_heatmap():
    try:
        logger.info("Fetching current market heatmap data...")
        engine = get_db_connection()
        query = text("""
            SELECT 
                TO_CHAR(date, 'YYYY-MM') as date,
                MAX(CASE WHEN region_name = 'New York' THEN price_yoy * 100 END) as "New York_YoY",
                MAX(CASE WHEN region_name = 'Los Angeles' THEN price_yoy * 100 END) as "Los Angeles_YoY",
                MAX(CASE WHEN region_name = 'Chicago' THEN price_yoy * 100 END) as "Chicago_YoY",
                MAX(CASE WHEN region_name = 'Dallas' THEN price_yoy * 100 END) as "Dallas_YoY",
                MAX(CASE WHEN region_name = 'Miami' THEN price_yoy * 100 END) as "Miami_YoY"
            FROM 
                zillow_housing
            WHERE
                date = (SELECT MAX(date) FROM zillow_housing)
                AND region_name IN ('New York', 'Los Angeles', 'Chicago', 'Dallas', 'Miami')
                AND price_yoy IS NOT NULL
            GROUP BY 
                date;
        """)
        logger.debug(f"Executing current market heatmap query: {query}")
        df = pd.read_sql(query, engine)
        if len(df) == 0:
            logger.warning("No current market heatmap data found")
            raise HTTPException(status_code=404, detail="No current market heatmap data found")
        logger.info(f"Market heatmap query executed successfully. Row count: {len(df)}")
        logger.debug(f"DataFrame content: \n{df}")

        record = df.to_dict(orient='records')[0]
        
        market_rates = {
            col.replace('_YoY', ''): float(val) if pd.notna(val) else None
            for col, val in record.items() 
            if col.endswith('_YoY')
        }
        
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
        error_msg = f"Error fetching current market heatmap: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mabspro.github.io",  # Frontend hosted on GitHub Pages
        "http://localhost:3000",  # Local frontend for development
        "http://localhost:3001",
        "https://housing-project-r7jbm7l0e-mabvuto-kaelas-projects.vercel.app",  # Vercel deployment
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
