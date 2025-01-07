import pandas as pd
import os
from pathlib import Path
import json
from datetime import datetime

class DataInspector:
    def __init__(self):
        """Initialize data inspector"""
        self.data_dir = Path('data')
        self.report = {
            'inspection_time': datetime.now().isoformat(),
            'datasets': {}
        }

    def inspect_bls_data(self):
        """Inspect BLS housing CPI data"""
        df = pd.read_csv('data/bls/bls_housing_processed.csv')
        dataset_report = {
            'file': 'bls_housing_processed.csv',
            'row_count': len(df),
            'column_count': len(df.columns),
            'duplicates': {},
            'missing_values': {},
            'date_format_issues': [],
            'numeric_issues': []
        }

        # Check for duplicates in date
        duplicates = df[df.duplicated(['date'], keep=False)]
        if not duplicates.empty:
            dataset_report['duplicates']['date'] = duplicates['date'].tolist()

        # Check date format
        try:
            pd.to_datetime(df['date'])
        except Exception as e:
            dataset_report['date_format_issues'].append(str(e))

        # Check numeric columns
        numeric_cols = ['Fuels_Utilities', 'Household_Furnishings', 'Housing', 'Housing_All', 'Shelter']
        for col in numeric_cols:
            non_numeric = df[pd.to_numeric(df[col], errors='coerce').isna()][col]
            if not non_numeric.empty:
                dataset_report['numeric_issues'].append(f"{col}: {len(non_numeric)} non-numeric values")

        # Check missing values
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                dataset_report['missing_values'][col] = int(missing)

        self.report['datasets']['bls'] = dataset_report

    def inspect_census_data(self):
        """Inspect Census housing data"""
        df = pd.read_csv('data/census/census_housing_processed.csv')
        dataset_report = {
            'file': 'census_housing_processed.csv',
            'row_count': len(df),
            'column_count': len(df.columns),
            'duplicates': {},
            'missing_values': {},
            'numeric_issues': []
        }

        # Check for duplicates in state/year combination
        duplicates = df[df.duplicated(['state', 'year'], keep=False)]
        if not duplicates.empty:
            dataset_report['duplicates']['state_year'] = duplicates[['state', 'year']].values.tolist()

        # Check numeric columns
        numeric_cols = [
            'Total_Housing_Units', 'Occupied_Units', 'Vacant_Units',
            'Owner_Occupied', 'Renter_Occupied', 'Median_Home_Value',
            'Median_Monthly_Housing_Cost', 'Vacancy_Rate', 'Homeownership_Rate'
        ]
        for col in numeric_cols:
            non_numeric = df[pd.to_numeric(df[col], errors='coerce').isna()][col]
            if not non_numeric.empty:
                dataset_report['numeric_issues'].append(f"{col}: {len(non_numeric)} non-numeric values")

        # Check missing values
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                dataset_report['missing_values'][col] = int(missing)

        self.report['datasets']['census'] = dataset_report

    def inspect_kaggle_housing_prices(self):
        """Inspect Kaggle housing prices data"""
        df = pd.read_csv('data/kaggle/housing/kaggle_housing_processed.csv')
        dataset_report = {
            'file': 'kaggle_housing_processed.csv',
            'row_count': len(df),
            'column_count': len(df.columns),
            'duplicates': {},
            'missing_values': {},
            'date_format_issues': [],
            'numeric_issues': []
        }

        # Check for duplicates in date
        duplicates = df[df.duplicated(['date'], keep=False)]
        if not duplicates.empty:
            dataset_report['duplicates']['date'] = duplicates['date'].tolist()

        # Check date format
        try:
            pd.to_datetime(df['date'])
        except Exception as e:
            dataset_report['date_format_issues'].append(str(e))

        # Check numeric columns
        numeric_cols = ['U.S. National', '20-City Composite', '10-City Composite']
        for col in numeric_cols:
            non_numeric = df[pd.to_numeric(df[col], errors='coerce').isna()][col]
            if not non_numeric.empty:
                dataset_report['numeric_issues'].append(f"{col}: {len(non_numeric)} non-numeric values")

        # Check missing values
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                dataset_report['missing_values'][col] = int(missing)

        self.report['datasets']['kaggle_housing'] = dataset_report

    def inspect_wages_data(self):
        """Inspect wages by education data"""
        df = pd.read_csv('data/kaggle/wages/kaggle_wages_processed.csv')
        dataset_report = {
            'file': 'kaggle_wages_processed.csv',
            'row_count': len(df),
            'column_count': len(df.columns),
            'duplicates': {},
            'missing_values': {},
            'numeric_issues': []
        }

        # Check for duplicates in Year and category combinations
        value_cols = [col for col in df.columns if col != 'Year']
        for col in value_cols:
            duplicates = df[df.duplicated(['Year', col], keep=False)]
            if not duplicates.empty:
                dataset_report['duplicates'][f'year_{col}'] = duplicates[['Year', col]].values.tolist()

        # Check numeric values
        for col in value_cols:
            non_numeric = df[pd.to_numeric(df[col], errors='coerce').isna()][col]
            if not non_numeric.empty:
                dataset_report['numeric_issues'].append(f"{col}: {len(non_numeric)} non-numeric values")

        # Check missing values
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                dataset_report['missing_values'][col] = int(missing)

        self.report['datasets']['wages'] = dataset_report

    def inspect_interest_rates(self):
        """Inspect interest rates data"""
        df = pd.read_csv('data/kaggle/interest_rates/kaggle_interest_rates_processed.csv')
        dataset_report = {
            'file': 'kaggle_interest_rates_processed.csv',
            'row_count': len(df),
            'column_count': len(df.columns),
            'duplicates': {},
            'missing_values': {},
            'date_format_issues': [],
            'numeric_issues': []
        }

        # Check for duplicates in date
        duplicates = df[df.duplicated(['Date'], keep=False)]
        if not duplicates.empty:
            dataset_report['duplicates']['date'] = duplicates['Date'].tolist()

        # Check date format
        try:
            pd.to_datetime(df['Date'])
        except Exception as e:
            dataset_report['date_format_issues'].append(str(e))

        # Check numeric columns
        numeric_cols = [
            'Federal Funds Target Rate', 'Federal Funds Upper Target',
            'Federal Funds Lower Target', 'Effective Federal Funds Rate',
            'Real GDP (Percent Change)', 'Unemployment Rate', 'Inflation Rate'
        ]
        for col in numeric_cols:
            non_numeric = df[pd.to_numeric(df[col], errors='coerce').isna()][col]
            if not non_numeric.empty:
                dataset_report['numeric_issues'].append(f"{col}: {len(non_numeric)} non-numeric values")

        # Check missing values
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                dataset_report['missing_values'][col] = int(missing)

        self.report['datasets']['interest_rates'] = dataset_report

    def inspect_zillow_data(self):
        """Inspect Zillow housing data"""
        df = pd.read_csv('data/kaggle/zillow/kaggle_zillow_processed.csv')
        dataset_report = {
            'file': 'kaggle_zillow_processed.csv',
            'row_count': len(df),
            'column_count': len(df.columns),
            'duplicates': {},
            'missing_values': {},
            'date_format_issues': [],
            'numeric_issues': []
        }

        # Check for duplicates in date/region combination
        duplicates = df[df.duplicated(['Date', 'RegionName'], keep=False)]
        if not duplicates.empty:
            dataset_report['duplicates']['date_region'] = duplicates[['Date', 'RegionName']].values.tolist()

        # Check date format
        try:
            pd.to_datetime(df['Date'])
        except Exception as e:
            dataset_report['date_format_issues'].append(str(e))

        # Check numeric columns
        numeric_cols = ['Price', 'Price_MoM', 'Price_YoY']
        for col in numeric_cols:
            non_numeric = df[pd.to_numeric(df[col], errors='coerce').isna()][col]
            if not non_numeric.empty:
                dataset_report['numeric_issues'].append(f"{col}: {len(non_numeric)} non-numeric values")

        # Check missing values
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                dataset_report['missing_values'][col] = int(missing)

        self.report['datasets']['zillow'] = dataset_report

    def inspect_zillow_hvi(self):
        """Inspect Zillow Home Value Index data"""
        df = pd.read_csv('data/kaggle/zillow_hvindex/kaggle_zillow_hvindex_processed.csv')
        dataset_report = {
            'file': 'kaggle_zillow_hvindex_processed.csv',
            'row_count': len(df),
            'column_count': len(df.columns),
            'duplicates': {},
            'missing_values': {},
            'date_format_issues': [],
            'numeric_issues': []
        }

        # Check date column format
        date_col = 'index' if 'index' in df.columns else 'Date'
        try:
            pd.to_datetime(df[date_col])
        except Exception as e:
            dataset_report['date_format_issues'].append(str(e))

        # Check numeric values in state columns
        state_cols = [col for col in df.columns if col not in ['index', 'Date']]
        for col in state_cols:
            non_numeric = df[pd.to_numeric(df[col], errors='coerce').isna()][col]
            if not non_numeric.empty:
                dataset_report['numeric_issues'].append(f"{col}: {len(non_numeric)} non-numeric values")

        # Check missing values
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                dataset_report['missing_values'][col] = int(missing)

        self.report['datasets']['zillow_hvi'] = dataset_report

    def inspect_all(self):
        """Run all inspections and save report"""
        print("Starting data inspection...")
        
        # Run all inspections
        self.inspect_bls_data()
        self.inspect_census_data()
        self.inspect_kaggle_housing_prices()
        self.inspect_wages_data()
        self.inspect_interest_rates()
        self.inspect_zillow_data()
        self.inspect_zillow_hvi()
        
        # Save report
        report_path = Path('data/inspection_report.json')
        with open(report_path, 'w') as f:
            json.dump(self.report, f, indent=2)
        
        print(f"\nInspection complete. Report saved to {report_path}")
        
        # Print summary of issues found
        print("\nSummary of issues found:")
        for dataset, report in self.report['datasets'].items():
            issues = []
            if report['duplicates']:
                issues.append(f"duplicates found")
            if report['missing_values']:
                issues.append(f"missing values found")
            if report.get('date_format_issues'):
                issues.append(f"date format issues found")
            if report['numeric_issues']:
                issues.append(f"numeric issues found")
            
            if issues:
                print(f"\n{dataset}:")
                for issue in issues:
                    print(f"  - {issue}")

def main():
    inspector = DataInspector()
    inspector.inspect_all()

if __name__ == "__main__":
    main()
