import requests
import pandas as pd
import os
from datetime import datetime
import json
import time
from dotenv import load_dotenv

class BLSHousingScraper:
    def __init__(self, api_key=None):
        """Initialize BLS scraper with optional API key"""
        self.base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
        self.api_key = api_key
        self.headers = {'Content-type': 'application/json'}
        
        # Load environment variables from the correct location
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                 'housing-dashboard', 'api', '.env.production')
        load_dotenv(dotenv_path)
        
        # Create data directory if it doesn't exist
        os.makedirs('data/bls', exist_ok=True)
        
        # Series IDs for housing-related data
        self.series_ids = {
            'CUUR0000SEHA': 'Housing',  # Consumer Price Index - Housing
            'CUUR0000SAH': 'Housing_All',  # Housing, All Items
            'CUUR0000SAH1': 'Shelter',  # Shelter
            'CUUR0000SAH2': 'Fuels_Utilities',  # Fuels and utilities
            'CUUR0000SAH3': 'Household_Furnishings',  # Household furnishings and operations
        }

    def fetch_data(self, start_year, end_year=None):
        """Fetch housing data from BLS API"""
        if end_year is None:
            end_year = datetime.now().year

        data = []
        
        # BLS API allows 50 series per request
        payload = {
            "seriesid": list(self.series_ids.keys()),
            "startyear": str(start_year),
            "endyear": str(end_year),
            "registrationkey": self.api_key
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()
            json_data = response.json()

            if json_data.get('status') != 'REQUEST_SUCCEEDED':
                print(f"Error: {json_data.get('message', 'Unknown error')}")
                return None

            # Process each series
            for series in json_data['Results']['series']:
                series_id = series['seriesID']
                series_name = self.series_ids[series_id]
                
                for item in series['data']:
                    year = item['year']
                    period = item['period'].replace('M', '')  # Convert M01 to 1
                    value = item['value']
                    
                    data.append({
                        'date': f"{year}-{period}",
                        'series_id': series_id,
                        'series_name': series_name,
                        'value': value
                    })

            return pd.DataFrame(data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def save_to_csv(self, df, filename=None):
        """Save data to CSV file"""
        if df is None or df.empty:
            print("No data to save")
            return

        if filename is None:
            filename = f"bls_housing_data_{datetime.now().strftime('%Y%m%d')}.csv"

        filepath = os.path.join('data', 'bls', filename)
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")

    def process_data(self, df):
        """Process and clean the BLS data"""
        if df is None or df.empty:
            return None

        # Convert date strings to datetime
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m')
        
        # Pivot the data to create columns for each series
        df_pivot = df.pivot(index='date', 
                          columns='series_name', 
                          values='value')
        
        # Reset index to make date a column
        df_pivot.reset_index(inplace=True)
        
        # Sort by date
        df_pivot.sort_values('date', inplace=True)
        
        return df_pivot

def main():
    # Initialize scraper (add your API key if you have one)
    scraper = BLSHousingScraper(api_key=os.getenv('BLS_API_KEY'))
    
    # Fetch last 10 years of data
    current_year = datetime.now().year
    df = scraper.fetch_data(current_year - 10, current_year)
    
    if df is not None:
        # Process the data
        df_processed = scraper.process_data(df)
        
        # Save both raw and processed data
        scraper.save_to_csv(df, 'bls_housing_raw.csv')
        if df_processed is not None:
            scraper.save_to_csv(df_processed, 'bls_housing_processed.csv')

if __name__ == "__main__":
    main()
