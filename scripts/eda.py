import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

def create_db_connection():
    """Create a SQLAlchemy database connection"""
    password = quote_plus(os.getenv('DB_PASSWORD'))
    db_url = f"postgresql://{os.getenv('DB_USER')}:{password}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(db_url)

def load_cleaned_data():
    """Load cleaned data from PostgreSQL"""
    engine = create_db_connection()
    query = "SELECT * FROM housing_prices_cleaned;"
    df = pd.read_sql(query, engine)
    df['date'] = pd.to_datetime(df['date'])
    return df

def apply_global_styling():
    """Apply consistent styling to all plots"""
    plt.style.use('seaborn-v0_8')
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 18,
        'axes.labelsize': 14,
        'legend.fontsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.figsize': (16, 9),
        'figure.dpi': 300
    })

def plot_national_trends(df):
    """Plot national housing price trends with event annotations"""
    apply_global_styling()
    plt.figure(figsize=(16, 10))  # Increased height for better spacing
    
    # Main plot with improved styling
    plt.plot(df['date'], df['U.S. National'], label='U.S. National', color='blue', linewidth=2)
    plt.title('U.S. National Housing Price Trends', pad=20)
    plt.xlabel('Date', labelpad=10)
    plt.ylabel('Normalized Price Index', labelpad=10)

    # Enhanced event annotations
    plt.axvline(pd.to_datetime('2008-09-15'), color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    plt.text(pd.to_datetime('2008-09-15'), df['U.S. National'].max() * 0.95, 
             '2008 Financial Crisis', color='red', fontsize=10, ha='left', va='center',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
             
    plt.axvline(pd.to_datetime('2020-03-11'), color='green', linestyle='--', alpha=0.5, linewidth=1.5)
    plt.text(pd.to_datetime('2020-03-11'), df['U.S. National'].max() * 0.85, 
             'COVID-19 Pandemic', color='green', fontsize=10, ha='left', va='center',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
    
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.4)

    # Enhanced caption with better positioning and formatting
    caption = ("This graph shows the evolution of U.S. national housing prices over time, "
              "highlighting significant economic events that impacted the housing market. "
              "The normalized price index allows for relative comparison across different time periods.")
    
    plt.subplots_adjust(bottom=0.15)
    plt.figtext(0.5, 0.02, caption, 
                wrap=True, 
                horizontalalignment='center', 
                fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=3))

    plt.savefig('dashboards/national_trends_refined_with_caption.png', bbox_inches='tight', dpi=300)
    plt.close()

def plot_growth_rates(df):
    """Plot year-over-year growth rates"""
    apply_global_styling()
    
    # Create figure with adjusted size and margins
    plt.figure(figsize=(16, 10))  # Increased height for better spacing
    
    # Create main plot
    for col in df.columns:
        if col.endswith('_YoY'):
            plt.plot(df['date'], df[col], label=col.replace('_YoY', ''), linewidth=1.5)  # Reduced line width
    
    plt.title('Year-over-Year Growth Rates', pad=20)
    plt.xlabel('Date', labelpad=10)
    plt.ylabel('Growth Rate (Year-over-Year %)', labelpad=10)  # Improved y-axis label

    # Improved legend positioning and formatting
    plt.legend(title='Markets', 
              fontsize=8,  # Reduced font size
              title_fontsize=10,
              loc='center left',  # Moved to left side
              bbox_to_anchor=(1.02, 0.5),  # Position outside of plot
              ncol=1,  # Single column for better readability
              borderaxespad=0)

    plt.grid(True, linestyle='--', alpha=0.4)  # Reduced grid prominence

    # Adjust layout to accommodate legend and caption
    plt.subplots_adjust(right=0.85, bottom=0.15)  # Make room for legend and caption

    # Enhanced caption with better positioning and formatting
    caption = ("This plot shows the Year-over-Year growth rates for various housing markets, "
              "revealing market trends and volatility across different regions. "
              "Positive values indicate price appreciation while negative values show price decline.")
    
    plt.figtext(0.5, 0.02, caption, 
                wrap=True, 
                horizontalalignment='center', 
                fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=3))

    # Save with tight layout and high DPI
    plt.savefig('dashboards/growth_rates_with_caption.png', bbox_inches='tight', dpi=300)
    plt.close()

def plot_selected_city_trends(df):
    """Plot trends for selected major cities"""
    apply_global_styling()
    selected_cities = [col for col in df.columns if col.startswith(('CA-', 'NY-', 'WA-', 'TX-', 'FL-'))][:5]
    plt.figure(figsize=(16, 10))  # Increased height for better spacing
    
    # Create main plot with improved styling
    for city in selected_cities:
        plt.plot(df['date'], df[city], label=city, linewidth=1.5)
    
    plt.title('Selected Major City Housing Price Trends', pad=20)
    plt.xlabel('Date', labelpad=10)
    plt.ylabel('Normalized Price Index', labelpad=10)
    
    # Improved legend positioning and formatting
    plt.legend(title='Cities', 
              fontsize=10,
              title_fontsize=12,
              loc='center left',
              bbox_to_anchor=(1.02, 0.5),
              borderaxespad=0)
    
    plt.grid(True, linestyle='--', alpha=0.4)

    # Enhanced caption with better positioning and formatting
    caption = ("This plot compares housing price trends across selected major U.S. cities, "
              "showing how different metropolitan areas have experienced varying patterns of "
              "price changes over time. The normalized index enables direct comparison between cities.")
    
    plt.subplots_adjust(right=0.85, bottom=0.15)  # Make room for legend and caption
    plt.figtext(0.5, 0.02, caption, 
                wrap=True, 
                horizontalalignment='center', 
                fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=3))

    plt.savefig('dashboards/selected_city_trends_with_caption.png', bbox_inches='tight', dpi=300)
    plt.close()

def identify_hot_cold_markets(df):
    """Heatmap of average YoY growth rates by market"""
    apply_global_styling()
    growth_rates = df[[col for col in df.columns if col.endswith('_YoY')]].mean().to_frame(name='Average YoY Growth')
    growth_rates = growth_rates.sort_values(by='Average YoY Growth', ascending=False)
    
    plt.figure(figsize=(12, 14))  # Adjusted size for better readability
    
    # Enhanced heatmap with improved formatting
    sns.heatmap(growth_rates, 
                annot=True, 
                fmt='.2%',  # Format as percentage
                cmap='coolwarm',
                center=0,  # Center colormap at 0
                cbar_kws={'label': 'Average YoY Growth Rate', 'format': '%.1%'})
    
    plt.title('Market Growth Rate Analysis', pad=20)
    plt.xlabel('Average Growth Rate', labelpad=10)
    plt.ylabel('Market', labelpad=10)

    # Enhanced caption with better positioning and formatting
    caption = ("This heatmap visualizes the average Year-over-Year growth rates across different markets. "
              "Red indicates higher growth rates while blue shows lower growth. "
              "Markets are sorted from highest to lowest average growth rate.")
    
    plt.subplots_adjust(bottom=0.15, right=0.95)
    plt.figtext(0.5, 0.02, caption, 
                wrap=True, 
                horizontalalignment='center', 
                fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=3))

    plt.savefig('dashboards/hot_cold_markets_with_caption.png', bbox_inches='tight', dpi=300)
    plt.close()

def plot_regional_comparison(df):
    """Compare housing prices across regions"""
    apply_global_styling()
    regional_columns = [col for col in df.columns if not col.endswith(('_MoM', '_YoY'))]
    regional_columns = [col for col in regional_columns if col.startswith(('CA-', 'NY-', 'WA-', 'TX-', 'FL-'))]
    regional_df = df[regional_columns]

    plt.figure(figsize=(16, 10))  # Adjusted size for better visibility
    
    # Enhanced boxplot with improved styling
    sns.boxplot(data=regional_df, 
                palette="RdYlBu_r",  # Changed color palette for better contrast
                width=0.7)  # Adjusted box width
    
    plt.title('Regional Housing Price Distribution', pad=20)
    plt.xlabel('Metropolitan Areas', labelpad=10)
    plt.ylabel('Normalized Price Index', labelpad=10)
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    
    # Improved median value annotations
    medians = regional_df.median()
    for i, median in enumerate(medians):
        plt.text(i, median, f'{median:.2f}', 
                ha='center', 
                va='bottom',
                color='black',
                fontsize=9,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Enhanced caption with better positioning and formatting
    caption = ("This boxplot displays the distribution of housing prices across different metropolitan areas. "
              "The boxes show the quartile ranges, with whiskers extending to the full price range. "
              "Median values are annotated for each region.")
    
    plt.subplots_adjust(bottom=0.25)  # Adjusted for rotated labels and caption
    plt.figtext(0.5, 0.02, caption, 
                wrap=True, 
                horizontalalignment='center', 
                fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=3))

    plt.savefig('dashboards/regional_comparison_filtered.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == "__main__":
    os.makedirs('dashboards', exist_ok=True)
    print("Loading cleaned data...")
    df = load_cleaned_data()
    
    print("Creating national trends plot...")
    plot_national_trends(df)
    
    print("Creating selected city trends plot...")
    plot_selected_city_trends(df)
    
    print("Creating growth rates plot...")
    plot_growth_rates(df)
    
    print("Creating regional comparison plot...")
    plot_regional_comparison(df)
    
    print("Identifying hot and cold markets...")
    identify_hot_cold_markets(df)
    
    print("EDA complete! Visualizations saved to dashboards/ directory.")
