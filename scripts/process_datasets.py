import os
import pandas as pd
from data_cleaning import (
    clean_kaggle_housing,
    clean_wages,
    clean_interest_rates,
    clean_zillow,
    clean_zillow_hvi,
    inspect_data
)

# Define file paths
datasets = {
    "kaggle_housing": "data/kaggle/housing/kaggle_housing_raw.csv",
    "wages": "data/kaggle/wages/kaggle_wages_raw.csv",
    "interest_rates": "data/kaggle/interest_rates/kaggle_interest_rates_raw.csv",
    "zillow": "data/kaggle/zillow/kaggle_zillow_raw.csv",
    "zillow_hvi": "data/kaggle/zillow_hvindex/kaggle_zillow_hvindex_raw.csv",
    "bls": "data/bls/bls_housing_raw.csv",
    "census": "data/census/census_housing_raw.csv"
}

# Define cleaning functions
cleaning_functions = {
    "kaggle_housing": clean_kaggle_housing,
    "wages": clean_wages,
    "interest_rates": clean_interest_rates,
    "zillow": clean_zillow,
    "zillow_hvi": clean_zillow_hvi,
    "bls": clean_kaggle_housing,  # Using similar cleaning strategy as housing data
    "census": clean_kaggle_housing  # Using similar cleaning strategy as housing data
}

def process_dataset(dataset_name, file_path):
    """
    Process a single dataset through the cleaning pipeline.
    
    Args:
        dataset_name (str): Name of the dataset
        file_path (str): Path to the dataset file
    """
    print(f"Processing {dataset_name}...")
    
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
        
        # Get initial data quality metrics
        initial_summary = inspect_data(df)
        print(f"Initial Summary: {initial_summary}")

        # Clean the data using the appropriate cleaning function
        cleaned_df = cleaning_functions[dataset_name](df)
        
        # Get final data quality metrics
        final_summary = inspect_data(cleaned_df)
        print(f"Final Summary: {final_summary}")

        # Create output directory if it doesn't exist
        os.makedirs("cleaned_data", exist_ok=True)
        
        # Save the cleaned dataset
        cleaned_file_path = f"data/cleaned/{dataset_name}_cleaned.csv"
        cleaned_df.to_csv(cleaned_file_path, index=False)
        print(f"Cleaned dataset saved to {cleaned_file_path}")
        
        # Print improvement metrics
        print(f"Improvements:")
        print(f"- Missing values reduced by: {initial_summary['missing_values'] - final_summary['missing_values']}")
        print(f"- Duplicates removed: {initial_summary['duplicates'] - final_summary['duplicates']}")
        print(f"- Numeric issues resolved: {initial_summary['numeric_issues'] - final_summary['numeric_issues']}\n")
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error processing {dataset_name}: {str(e)}")

def main():
    """
    Main function to process all datasets through the cleaning pipeline.
    """
    print("Starting data cleaning process...\n")
    
    for dataset_name, file_path in datasets.items():
        process_dataset(dataset_name, file_path)
    
    print("Data cleaning process completed!")

if __name__ == "__main__":
    main()
