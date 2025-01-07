import pandas as pd
import numpy as np

def handle_missing_values(df, strategy="drop", fill_value=None):
    """
    Handle missing values in the dataset.
    Args:
        df (pd.DataFrame): The DataFrame to process.
        strategy (str): "drop" to remove rows, "fill" to fill missing values.
        fill_value: Value to fill if strategy is "fill".
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    if strategy == "drop":
        return df.dropna()
    elif strategy == "fill":
        return df.fillna(fill_value)
    elif strategy == "mean":
        return df.fillna(df.mean(numeric_only=True))
    else:
        raise ValueError("Invalid strategy! Use 'drop', 'fill', or 'mean'.")

def handle_numeric_issues(df):
    """
    Fix numeric issues by coercing columns to numeric and replacing invalid values.
    Args:
        df (pd.DataFrame): The DataFrame to process.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    for col in df.select_dtypes(include=["object", "float", "int"]).columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def remove_duplicates(df):
    """
    Remove duplicate rows from the dataset.
    Args:
        df (pd.DataFrame): The DataFrame to process.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    return df.drop_duplicates()

def inspect_data(df):
    """
    Inspect the dataset for summary information.
    Args:
        df (pd.DataFrame): The DataFrame to inspect.
    Returns:
        dict: Summary of issues in the dataset.
    """
    return {
        "missing_values": df.isnull().sum().sum(),
        "duplicates": df.duplicated().sum(),
        "numeric_issues": (df.select_dtypes(include=[np.number]).isna().sum().sum())
    }

def clean_kaggle_housing(df):
    """
    Clean Kaggle housing dataset.
    Args:
        df (pd.DataFrame): The DataFrame to clean.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Handle missing values by filling with mean
    df = handle_missing_values(df, strategy="mean")
    return df

def clean_wages(df):
    """
    Clean wages dataset.
    Args:
        df (pd.DataFrame): The DataFrame to clean.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Handle missing values by filling with median
    df = handle_missing_values(df, strategy="fill", fill_value=df.median(numeric_only=True))
    # Fix numeric issues
    df = handle_numeric_issues(df)
    return df

def clean_interest_rates(df):
    """
    Clean interest rates dataset.
    Args:
        df (pd.DataFrame): The DataFrame to clean.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Handle missing values by dropping rows
    df = handle_missing_values(df, strategy="drop")
    # Fix numeric issues
    df = handle_numeric_issues(df)
    return df

def clean_zillow(df):
    """
    Clean Zillow dataset.
    Args:
        df (pd.DataFrame): The DataFrame to clean.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Remove duplicates
    df = remove_duplicates(df)
    # Handle missing values
    df = handle_missing_values(df, strategy="mean")
    # Fix numeric issues
    df = handle_numeric_issues(df)
    return df

def clean_zillow_hvi(df):
    """
    Clean Zillow Home Value Index dataset.
    Args:
        df (pd.DataFrame): The DataFrame to clean.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Ensure we have proper date information
    if 'Date' in df.columns:
        df['date'] = pd.to_datetime(df['Unnamed: 0'])
        df = df.drop(['Date', 'Unnamed: 0'], axis=1)
    elif 'Unnamed: 0' in df.columns:
        df['date'] = pd.to_datetime(df['Unnamed: 0'])
        df = df.drop('Unnamed: 0', axis=1)
    
    # First convert to numeric to ensure proper handling
    df = handle_numeric_issues(df)
    
    # Forward fill missing values within each group/region
    # This assumes missing values should use the last known value
    for col in df.select_dtypes(include=[np.number]).columns:
        if col != 'date':  # Skip the date column
            df[col] = df[col].ffill()
    
    # If any remaining missing values, use backward fill
    df = df.bfill()
    
    # If still any missing values (e.g., completely empty columns)
    # fill with 0 as last resort
    df = df.fillna(0)
    
    return df

def clean_dataset(df, missing_strategy="drop", fill_value=None, time_series=False):
    """
    Apply a complete cleaning pipeline to the dataset.
    Args:
        df (pd.DataFrame): The DataFrame to clean.
        missing_strategy (str): Strategy for handling missing values.
        fill_value: Value to use if missing_strategy is "fill".
    Returns:
        pd.DataFrame: The fully cleaned DataFrame.
        dict: Summary of cleaning operations performed.
    """
    # Store initial state for reporting
    initial_state = inspect_data(df)
    
    # Apply cleaning operations
    df = handle_numeric_issues(df)
    
    if time_series:
        # For time series data, try forward/backward fill first
        df = df.ffill().bfill()
        # Then apply standard missing value handling for any remaining NAs
        df = handle_missing_values(df, strategy=missing_strategy, fill_value=fill_value)
    else:
        df = handle_missing_values(df, strategy=missing_strategy, fill_value=fill_value)
    
    df = remove_duplicates(df)
    
    # Store final state for reporting
    final_state = inspect_data(df)
    
    # Create summary report
    summary = {
        "initial_issues": initial_state,
        "final_issues": final_state,
        "rows_removed": len(df) - len(df),
        "cleaning_operations": [
            "numeric_conversion",
            f"missing_values_{missing_strategy}",
            "duplicate_removal"
        ]
    }
    
    return df, summary
