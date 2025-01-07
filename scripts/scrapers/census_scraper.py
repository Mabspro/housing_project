import requests
import pandas as pd
import os
from datetime import datetime
import time
from dotenv import load_dotenv

class CensusHousingScraper:
    def __init__(self, api_key=None):
        """Initialize Census scraper with optional API key"""
        self.base_url = "https://api.census.gov/data"
        self.api_key = api_key
        
        # Load environment variables from the correct location
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                 'housing-dashboard', 'api', '.env.production')
        load_dotenv(dotenv_path)
        
        # Create data directory if it doesn't exist
        os.makedirs('data/census', exist_ok=True)
        
        # Define variables to fetch
        self.variables = {
            'B25001_001E': 'Total_Housing_Units',
            'B25002_002E': 'Occupied_Units',
            'B25002_003E': 'Vacant_Units',
            'B25003_002E': 'Owner_Occupied',
            'B25003_003E': 'Renter_Occupied',
            'B25077_001E': 'Median_Home_Value',
            'B25105_001E': 'Median_Monthly_Housing_Cost'
        }
        
        # Define states to fetch data for
        self.states = {
            '06': 'California',
            '36': 'New York',
            '48': 'Texas',
            '12': 'Florida',
            '17': 'Illinois'
        }

    def fetch_data(self, year):
        """Fetch housing data from Census API for specified year"""
        data = []
        
        # Construct variable list for API
        var_list = list(self.variables.keys())
        variables = ['NAME'] + var_list
        
        # Create API URL
        url = f"{self.base_url}/{year}/acs/acs5"
        
        # Parameters for the API request
        params = {
            'get': ','.join(variables),
            'for': 'state:' + ','.join(self.states.keys()),
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            json_data = response.json()
            
            # First row contains headers
            headers = json_data[0]
            
            # Process each row of data
            for row in json_data[1:]:
                record = dict(zip(headers, row))
                state_fips = record['state']
                state_name = self.states.get(state_fips)
                
                if state_name:
                    entry = {
                        'state': state_name,
                        'year': year
                    }
                    
                    # Add each variable to the entry
                    for var_id, var_name in self.variables.items():
                        value = record.get(var_id)
                        try:
                            entry[var_name] = int(value) if value not in [None, ''] else None
                        except ValueError:
                            entry[var_name] = None
                    
                    data.append(entry)
            
            return pd.DataFrame(data)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {year}: {e}")
            return None

    def fetch_multiple_years(self, start_year, end_year=None):
        """Fetch data for multiple years"""
        if end_year is None:
            end_year = datetime.now().year - 1  # Previous year's data
        
        all_data = []
        
        for year in range(start_year, end_year + 1):
            print(f"Fetching data for {year}...")
            df = self.fetch_data(year)
            
            if df is not None:
                all_data.append(df)
            
            # Sleep to respect API rate limits
            time.sleep(1)
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return None

    def save_to_csv(self, df, filename=None):
        """Save data to CSV file"""
        if df is None or df.empty:
            print("No data to save")
            return

        if filename is None:
            filename = f"census_housing_data_{datetime.now().strftime('%Y%m%d')}.csv"

        filepath = os.path.join('data', 'census', filename)
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")

    def process_data(self, df):
        """Process and clean the Census data"""
        if df is None or df.empty:
            return None

        # Calculate derived metrics
        df['Vacancy_Rate'] = (df['Vacant_Units'] / df['Total_Housing_Units'] * 100).round(2)
        df['Homeownership_Rate'] = (df['Owner_Occupied'] / df['Occupied_Units'] * 100).round(2)
        
        # Sort by state and year
        df.sort_values(['state', 'year'], inplace=True)
        
        return df

def main():
    # Initialize scraper (add your API key if you have one)
    scraper = CensusHousingScraper(api_key=os.getenv('CENSUS_API_KEY'))
    
    # Fetch last 5 years of data
    current_year = datetime.now().year - 1  # Previous year's data
    df = scraper.fetch_multiple_years(current_year - 5, current_year)
    
    if df is not None:
        # Process the data
        df_processed = scraper.process_data(df)
        
        # Save both raw and processed data
        scraper.save_to_csv(df, 'census_housing_raw.csv')
        if df_processed is not None:
            scraper.save_to_csv(df_processed, 'census_housing_processed.csv')

if __name__ == "__main__":
    main()
