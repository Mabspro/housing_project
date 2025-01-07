# ETL Process Documentation

This document details the Extract, Transform, and Load processes for all data sources in the housing market analysis project.

## Process Overview

The ETL pipeline consists of three main stages:

1. **Extract** (Scraping/Download)
   - Files: 
     * `scripts/scrapers/bls_scraper.py`
     * `scripts/scrapers/census_scraper.py`
     * `scripts/scrapers/kaggle_scraper.py`
   - Downloads raw data from various sources
   - Saves to appropriate directories under `data/`

2. **Transform** (Cleaning/Processing)
   - Initial Processing:
     * Each scraper includes initial transformations
     * Saves to `*_processed.csv` files
   - Data Cleaning:
     * `scripts/data_cleaning.py`: Core cleaning functions
     * `scripts/process_datasets.py`: Orchestrates cleaning pipeline
     * Saves to `data/cleaned/` directory

3. **Load** (Database)
   - Files:
     * `scripts/drop_create_db.py`: Database initialization
     * `scripts/scrapers/schema.sql`: Database schema
     * `scripts/scrapers/load_to_db.py`: Data loading
   - Creates tables and loads cleaned data

## Data Sources and Processing

### BLS (Bureau of Labor Statistics) Data

#### Extraction
- Source: BLS API
- File: `bls_scraper.py`
- Output: `data/bls/bls_housing_raw.csv`

#### Initial Transform
- File: `bls_scraper.py`
- Output: `data/bls/bls_housing_processed.csv`
- Process:
  * Convert date strings to datetime
  * Sort chronologically
  * Calculate MoM/YoY changes

#### Cleaning
- File: `data_cleaning.py`
- Function: `clean_kaggle_housing()`
- Process:
  * Handle missing values using mean imputation
  * Validate numeric data
- Output: `data/cleaned/bls_cleaned.csv`

### Census Bureau Data

#### Extraction
- Source: Census Bureau API
- File: `census_scraper.py`
- Output: `data/census/census_housing_raw.csv`

#### Initial Transform
- File: `census_scraper.py`
- Output: `data/census/census_housing_processed.csv`
- Process:
  * Standardize dates
  * Calculate vacancy and homeownership rates

#### Cleaning
- File: `data_cleaning.py`
- Function: `clean_kaggle_housing()`
- Process:
  * Handle missing values
  * Validate numeric data
- Output: `data/cleaned/census_cleaned.csv`

### Kaggle Datasets

#### 1. Housing Prices Dataset
- Source: praveenchandran2006/u-s-housing-prices-regional-trends-2000-2023
- Files:
  * Extract: `kaggle_scraper.py`
  * Clean: `clean_kaggle_housing()`
- Process:
  * Download → `data/kaggle/housing/kaggle_housing_raw.csv`
  * Process → `data/kaggle/housing/kaggle_housing_processed.csv`
  * Clean → `data/cleaned/kaggle_housing_cleaned.csv`

#### 2. Wages Dataset
- Files:
  * Extract: `kaggle_scraper.py`
  * Clean: `clean_wages()`
- Process:
  * Download → `data/kaggle/wages/kaggle_wages_raw.csv`
  * Process → `data/kaggle/wages/kaggle_wages_processed.csv`
  * Clean → `data/cleaned/wages_cleaned.csv`

#### 3. Interest Rates Dataset
- Files:
  * Extract: `kaggle_scraper.py`
  * Clean: `clean_interest_rates()`
- Process:
  * Download → `data/kaggle/interest_rates/kaggle_interest_rates_raw.csv`
  * Process → `data/kaggle/interest_rates/kaggle_interest_rates_processed.csv`
  * Clean → `data/cleaned/interest_rates_cleaned.csv`

#### 4. Zillow Housing Dataset
- Files:
  * Extract: `kaggle_scraper.py`
  * Clean: `clean_zillow()`
- Process:
  * Download → `data/kaggle/zillow/kaggle_zillow_raw.csv`
  * Process → `data/kaggle/zillow/kaggle_zillow_processed.csv`
  * Clean → `data/cleaned/zillow_cleaned.csv`

#### 5. Zillow Home Value Index Dataset
- Files:
  * Extract: `kaggle_scraper.py`
  * Clean: `clean_zillow_hvi()`
- Process:
  * Download → `data/kaggle/zillow_hvindex/kaggle_zillow_hvindex_raw.csv`
  * Process → `data/kaggle/zillow_hvindex/kaggle_zillow_hvindex_processed.csv`
  * Clean → `data/cleaned/zillow_hvi_cleaned.csv`

## Cleaning Pipeline

### Core Cleaning Functions (`data_cleaning.py`)
1. `handle_missing_values()`: Multiple strategies (drop, fill, mean)
2. `handle_numeric_issues()`: Convert and validate numeric data
3. `remove_duplicates()`: Remove duplicate entries
4. `inspect_data()`: Generate data quality metrics

### Dataset-Specific Functions
- Each dataset has a dedicated cleaning function
- Implements appropriate cleaning strategy
- Handles dataset-specific requirements

### Processing Script (`process_datasets.py`)
- Orchestrates the cleaning pipeline
- Processes all datasets sequentially
- Generates cleaning reports
- Saves cleaned data to `data/cleaned/`

## Database Management

### Database Reset (`drop_create_db.py`)
1. Terminates existing connections
2. Drops existing database if present
3. Creates new database

### Schema Creation (`schema.sql`)
- Defines all table structures
- Creates appropriate indexes
- Sets up constraints

### Data Loading (`load_to_db.py`)
1. Creates tables using schema
2. Loads each dataset:
   - Reads cleaned data
   - Performs final transformations if needed
   - Loads into appropriate tables
3. Handles:
   - Column mapping
   - Data type conversion
   - Duplicate prevention
   - Error handling

### Database Backup (`backup_db.py`)
1. Creates timestamped SQL backup
2. Uses pg_dump for reliable backups
3. Saves to `backups/` directory
4. Backup format: `housing_db_backup_YYYYMMDD_HHMMSS.sql`
5. Includes:
   - Table structures
   - Indexes and constraints
   - All data

## Directory Structure

```
scripts/
├── data_cleaning.py          # Cleaning functions
├── process_datasets.py       # Cleaning pipeline
├── drop_create_db.py        # Database reset
├── backup_db.py             # Database backup
├── scrapers/
│   ├── bls_scraper.py       # BLS data extraction
│   ├── census_scraper.py    # Census data extraction
│   ├── kaggle_scraper.py    # Kaggle data extraction
│   ├── load_to_db.py        # Database loading
│   └── schema.sql           # Database schema
data/
├── bls/                     # BLS data files
├── census/                  # Census data files
├── kaggle/                  # Kaggle datasets
│   ├── housing/
│   ├── wages/
│   ├── interest_rates/
│   ├── zillow/
│   └── zillow_hvindex/
├── cleaned/                 # Cleaned datasets
└── backups/                 # Database backups
