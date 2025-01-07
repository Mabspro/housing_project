import pandas as pd

def check_data_file(filepath, description):
    print(f"\nChecking for duplicates in {description}...")
    
    # Read the data
    df = pd.read_csv(filepath)
    
    # Print total number of rows
    print(f"Total rows: {len(df)}")
    
    # Print column names
    print(f"Columns: {', '.join(df.columns.tolist())}")
    
    # Handle date columns
    if 'Date' in df.columns:
        print("\nDate column info:")
        print(df['Date'].describe())
    if 'Unnamed: 0' in df.columns:
        print("\nUnnamed: 0 column info:")
        print(df['Unnamed: 0'].describe())
    
    # Melt the data to check for duplicates
    state_cols = [col for col in df.columns if col not in ['Date', 'Unnamed: 0'] and not col.endswith('_MoM')]
    
    df_melted = pd.melt(
        df,
        id_vars=['Unnamed: 0'] if 'Unnamed: 0' in df.columns else ['Date'],
        value_vars=state_cols,
        var_name='state',
        value_name='home_value_index'
    )
    
    # Check for duplicates
    duplicates = df_melted[df_melted.duplicated(['Unnamed: 0' if 'Unnamed: 0' in df.columns else 'Date', 'state'], keep=False)]
    
    if len(duplicates) > 0:
        print(f"\nFound {len(duplicates)} duplicate entries!")
        print("\nSample of duplicates:")
        print(duplicates.sort_values(['Unnamed: 0' if 'Unnamed: 0' in df.columns else 'Date', 'state']).head(10))
    else:
        print("\nNo duplicates found after melting!")

def check_duplicates():
    # Check processed data
    df = pd.read_csv('data/kaggle/zillow_hvindex/kaggle_zillow_hvindex_processed.csv')
    
    # Convert index to datetime if it's a date column
    if 'index' in df.columns:
        df['date'] = pd.to_datetime(df['index'])
        df = df.drop('index', axis=1)
    elif 'Date' in df.columns:
        df['date'] = pd.to_datetime(df['Date'])
        df = df.drop('Date', axis=1)
    
    # Melt state columns into rows
    state_cols = [col for col in df.columns if col != 'date']
    df_melted = pd.melt(
        df,
        id_vars=['date'],
        value_vars=state_cols,
        var_name='state',
        value_name='home_value_index'
    )
    
    # Check for duplicates
    duplicates = df_melted[df_melted.duplicated(['date', 'state'], keep=False)]
    
    if len(duplicates) > 0:
        print(f"\nFound {len(duplicates)} duplicate entries!")
        print("\nSample of duplicates:")
        print(duplicates.sort_values(['date', 'state']).head(10))
        
        # Group by date and state to show counts
        dup_counts = duplicates.groupby(['date', 'state']).size().reset_index(name='count')
        print("\nDuplicate counts by date and state:")
        print(dup_counts.sort_values('count', ascending=False).head(10))
    else:
        print("No duplicates found!")

def main():
    # Check both processed and cleaned data
    check_data_file('data/kaggle/zillow_hvindex/kaggle_zillow_hvindex_processed.csv', 'processed Zillow HVI data')
    check_data_file('data/cleaned/zillow_hvi_cleaned.csv', 'cleaned Zillow HVI data')

if __name__ == "__main__":
    main()
