import kagglehub
import pandas as pd
import os
import shutil
from datetime import datetime

class KaggleHousingScraper:
    def __init__(self):
        """Initialize Kaggle scraper"""
        # Create data directory if it doesn't exist
        os.makedirs('data/kaggle', exist_ok=True)
        
        self.datasets = {
            "housing": "praveenchandran2006/u-s-housing-prices-regional-trends-2000-2023",
            "wages": "asaniczka/wages-by-education-in-the-usa-1973-2022",
            "interest_rates": "federalreserve/interest-rates",
            "zillow": "paultimothymooney/zillow-house-price-data",
            "zillow_hvindex": "robikscube/zillow-home-value-index"  # Home Value Index data
        }
        
    def fetch_data(self, dataset_key):
        """Download the latest version of the specified dataset"""
        if dataset_key not in self.datasets:
            print(f"Unknown dataset: {dataset_key}")
            return None
            
        dataset = self.datasets[dataset_key]
        print(f"Downloading dataset: {dataset}")
        try:
            # Download latest version
            path = kagglehub.dataset_download(dataset)
            print(f"Dataset downloaded to: {path}")
            return path
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            return None

    def process_data(self, file_path, dataset_key):
        """Process the downloaded CSV file based on dataset type"""
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)
            print(f"\nColumns in {dataset_key} dataset:")
            print(df.columns.tolist())
            
            if dataset_key == "housing":
                # Process housing data
                df = df.rename(columns={'Unnamed: 0': 'date'})
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                # Calculate month-over-month and year-over-year changes
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                changes = []
                for col in numeric_cols:
                    changes.append(pd.DataFrame({
                        f'{col}_MoM': df[col].pct_change(fill_method=None),
                        f'{col}_YoY': df[col].pct_change(12, fill_method=None)
                    }))
                
                # Combine all changes at once
                if changes:
                    changes_df = pd.concat(changes, axis=1)
                    df = pd.concat([df, changes_df], axis=1)
            
            elif dataset_key == "wages":
                # Process wages data
                df = df.rename(columns={'year': 'Year'})
                df['Year'] = pd.to_numeric(df['Year'])
                df = df.sort_values('Year')
                
                # Calculate year-over-year changes for all columns at once
                wage_cols = [col for col in df.columns if col != 'Year']
                changes = pd.DataFrame({
                    f'{col}_YoY': df[col].pct_change(fill_method=None)
                    for col in wage_cols
                })
                df = pd.concat([df, changes], axis=1)

            elif dataset_key == "interest_rates":
                # Process interest rates data
                # Combine Year, Month, Day into Date
                df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
                df = df.drop(['Year', 'Month', 'Day'], axis=1)
                df = df.sort_values('Date')
                
                # Calculate changes for all rate columns at once
                rate_cols = [col for col in df.columns if col != 'Date']
                changes = pd.DataFrame({
                    f'{col}_MoM': df[col].pct_change(fill_method=None)
                    for col in rate_cols
                })
                changes.update(pd.DataFrame({
                    f'{col}_YoY': df[col].pct_change(12, fill_method=None)
                    for col in rate_cols
                }))
                df = pd.concat([df, changes], axis=1)

            elif dataset_key == "zillow":
                # Process Zillow housing data
                # Melt the date columns into rows
                id_cols = ['RegionName', 'State', 'Metro', 'CountyName', 'SizeRank']
                date_cols = [col for col in df.columns if col not in id_cols + ['Unnamed: 0']]
                
                df = pd.melt(df, 
                           id_vars=id_cols,
                           value_vars=date_cols,
                           var_name='Date',
                           value_name='Price')
                
                # Convert date and sort
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values(['RegionName', 'Date'])
                
                # Calculate changes by region efficiently
                df['Price_MoM'] = df.groupby('RegionName')['Price'].transform(
                    lambda x: x.pct_change(fill_method=None))
                df['Price_YoY'] = df.groupby('RegionName')['Price'].transform(
                    lambda x: x.pct_change(12, fill_method=None))

            elif dataset_key == "zillow_hvindex":
                # Process Zillow Home Value Index data
                # Convert index to date if it's not already a column
                if 'date' not in df.columns and 'Date' not in df.columns:
                    df = df.reset_index()
                    df = df.rename(columns={'index': 'Date'})
                
                # Calculate changes for all states at once
                state_cols = [col for col in df.columns if col not in ['Date', 'Unnamed: 0']]
                changes = pd.DataFrame({
                    f'{col}_MoM': df[col].pct_change(fill_method=None)
                    for col in state_cols
                })
                changes.update(pd.DataFrame({
                    f'{col}_YoY': df[col].pct_change(12, fill_method=None)
                    for col in state_cols
                }))
                df = pd.concat([df, changes], axis=1)
            
            return df
        except Exception as e:
            print(f"Error processing data: {e}")
            return None

    def save_to_csv(self, df, dataset_key, filename=None):
        """Save data to CSV file"""
        if df is None or df.empty:
            print("No data to save")
            return

        if filename is None:
            filename = f"kaggle_{dataset_key}_data_{datetime.now().strftime('%Y%m%d')}.csv"

        filepath = os.path.join('data', 'kaggle', dataset_key, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")

    def run(self, dataset_key):
        """Run the complete scraping process for a specific dataset"""
        # Download data
        download_path = self.fetch_data(dataset_key)
        if not download_path:
            return
        
        # Find the CSV file in the downloaded directory
        csv_file = None
        for root, dirs, files in os.walk(download_path):
            for file in files:
                if file.endswith('.csv'):
                    csv_file = os.path.join(root, file)
                    break
            if csv_file:
                break
        
        if not csv_file:
            print("No CSV file found in downloaded dataset")
            return
        
        # Process data
        print("Processing data...")
        df = self.process_data(csv_file, dataset_key)
        
        if df is not None:
            # Save both raw and processed data
            print("Saving data...")
            # Save raw data
            raw_path = os.path.join('data', 'kaggle', dataset_key, f'kaggle_{dataset_key}_raw.csv')
            os.makedirs(os.path.dirname(raw_path), exist_ok=True)
            shutil.copy2(csv_file, raw_path)
            print(f"Raw data saved to: {raw_path}")
            
            # Save processed data
            self.save_to_csv(df, dataset_key, f'kaggle_{dataset_key}_processed.csv')
        
        # Clean up downloaded files
        print("Cleaning up downloaded files...")
        shutil.rmtree(download_path)

def main():
    scraper = KaggleHousingScraper()
    
    # Download and process all datasets
    for dataset in ["housing", "wages", "interest_rates", "zillow", "zillow_hvindex"]:
        print(f"\nProcessing {dataset} dataset...")
        scraper.run(dataset)

if __name__ == "__main__":
    main()
