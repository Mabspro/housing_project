# Housing Data Scrapers

This directory contains scrapers for collecting housing-related data from:
1. Bureau of Labor Statistics (BLS)
2. U.S. Census Bureau
3. Kaggle Housing Dataset

## Setup

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Set up environment variables for API keys:

The API keys should be added to `housing-dashboard/api/.env.production`. The file already contains placeholders for both API keys:
```
BLS_API_KEY=your_bls_api_key_here
CENSUS_API_KEY=your_census_api_key_here
```

Replace these placeholder values with your actual API keys.

### Getting API Keys

#### BLS API Key
1. Visit https://www.bls.gov/developers/
2. Register for a free API key
3. You'll receive the key via email

#### Census API Key
1. Visit https://api.census.gov/data/key_signup.html
2. Fill out the form
3. You'll receive the key via email

## Usage

### BLS Housing Data Scraper
```python
# Run the BLS scraper
python bls_scraper.py
```

This will:
- Fetch housing-related CPI data from BLS
- Save raw data to `data/bls/bls_housing_raw.csv`
- Save processed data to `data/bls/bls_housing_processed.csv`

Data includes:
- Housing CPI
- Shelter costs
- Fuels and utilities
- Household furnishings

### Census Housing Data Scraper
```python
# Run the Census scraper
python census_scraper.py
```

This will:
- Fetch housing data for major states from Census Bureau
- Save raw data to `data/census/census_housing_raw.csv`
- Save processed data to `data/census/census_housing_processed.csv`

Data includes:
- Total housing units
- Occupancy status
- Owner vs renter occupied
- Median home values
- Monthly housing costs

## Output

Data is saved in the following directories:
- `data/bls/` - BLS housing data
- `data/census/` - Census housing data

Each scraper produces two files:
1. Raw data directly from the API
2. Processed data with additional calculations and cleaning

### Kaggle Data Scraper
```python
# Run the Kaggle scraper
python kaggle_scraper.py
```

This will download and process five datasets:

1. Housing Prices Dataset:
   - Save raw data to `data/kaggle/housing/kaggle_housing_raw.csv`
   - Save processed data to `data/kaggle/housing/kaggle_housing_processed.csv`
   
   Data includes:
   - Historical housing prices from 2000-2023
   - Regional price trends
   - Month-over-month changes
   - Year-over-year changes

2. Wages Dataset:
   - Save raw data to `data/kaggle/wages/kaggle_wages_raw.csv`
   - Save processed data to `data/kaggle/wages/kaggle_wages_processed.csv`
   
   Data includes:
   - Wages by education level from 1973-2022
   - Year-over-year changes in wages
   - Education level breakdowns

3. Interest Rates Dataset:
   - Save raw data to `data/kaggle/interest_rates/kaggle_interest_rates_raw.csv`
   - Save processed data to `data/kaggle/interest_rates/kaggle_interest_rates_processed.csv`
   
   Data includes:
   - Federal Reserve interest rate data
   - Month-over-month rate changes
   - Year-over-year rate changes
   - Various interest rate types

4. Zillow Housing Dataset:
   - Save raw data to `data/kaggle/zillow/kaggle_zillow_raw.csv`
   - Save processed data to `data/kaggle/zillow/kaggle_zillow_processed.csv`
   
   Data includes:
   - Detailed house price data by region
   - Historical price trends
   - Month-over-month changes
   - Year-over-year changes
   - Regional market analysis

5. Zillow Home Value Index Dataset:
   - Save raw data to `data/kaggle/zillow_hvindex/kaggle_zillow_hvindex_raw.csv`
   - Save processed data to `data/kaggle/zillow_hvindex/kaggle_zillow_hvindex_processed.csv`
   
   Data includes:
   - Zillow's proprietary home value index
   - Granular regional price trends
   - Month-over-month changes
   - Year-over-year changes
   - Market value assessments

## Rate Limits

- BLS: 500 queries per day with registered key
- Census: 500 queries per second per key
- Kaggle: No specific rate limits for dataset downloads
