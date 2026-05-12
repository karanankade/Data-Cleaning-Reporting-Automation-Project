import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(filename="raw_sales_data.csv"):
    """Loads the messy data from a CSV file."""
    print(f"Loading data from {filename}...")
    try:
        df = pd.read_csv(filename)
        print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.\n")
        return df
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

def clean_data(df):
    """Cleans the dataframe according to business rules."""
    print("Starting data cleaning...")
    initial_rows = len(df)
    
    # 1. Handle Missing Values
    # Fill numeric columns with median
    if 'Quantity' in df.columns:
        df['Quantity'].fillna(df['Quantity'].median(), inplace=True)
    if 'Price' in df.columns:
        df['Price'].fillna(df['Price'].median(), inplace=True)
    
    # Fill categorical columns with mode
    if 'City' in df.columns:
        df['City'].fillna(df['City'].mode()[0], inplace=True)
        
    # 2. Remove Duplicates
    df.drop_duplicates(inplace=True)
    print(f"Removed {initial_rows - len(df)} duplicate rows.")
    
    # 3. Fix Inconsistent Text
    if 'City' in df.columns:
        df['City'] = df['City'].str.title().str.strip()
    if 'Product' in df.columns:
        df['Product'] = df['Product'].str.title().str.strip()
        
    # 4. Fix Date Format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        missing_dates = df['Date'].isnull().sum()
        df = df.dropna(subset=['Date']).copy()
        print(f"Dropped {missing_dates} rows with invalid dates.")
        
    # 5. Create New Business Columns
    df['Revenue'] = df['Quantity'] * df['Price']
    df['Month'] = df['Date'].dt.to_period('M')
    
    print(f"Data cleaning finished. {len(df)} rows remaining.\n")
    return df

def generate_insights(df):
    """Calculates KPI metrics and generates insights."""
    print("--- KPI Insights ---")
    total_revenue = df['Revenue'].sum()
    total_orders = df.shape[0]
    top_product = df.groupby('Product')['Revenue'].sum().idxmax()
    
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total Orders: {total_orders}")
    print(f"Top Performing Product: {top_product}\n")
    
def create_report(df, excel_filename="Automated_Report.xlsx", chart_filename="monthly_sales.png"):
    """Generates an Excel report and a monthly sales chart."""
    print(f"Generating reports...")
    
    # Create Monthly Sales Chart
    monthly_sales = df.groupby('Month')['Revenue'].sum()
    plt.figure(figsize=(10, 6))
    monthly_sales.plot(kind='bar', color='skyblue')
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(chart_filename)
    print(f"Saved chart to {chart_filename}.")
    
    # Create Automated Excel Report
    try:
        with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
            # Sheet 1: Cleaned Data
            # Convert 'Month' period back to string for Excel compatibility
            df_export = df.copy()
            df_export['Month'] = df_export['Month'].astype(str)
            df_export.to_excel(writer, sheet_name='Cleaned Data', index=False)
            
            # Sheet 2: Monthly Summary
            monthly_summary = monthly_sales.reset_index()
            monthly_summary['Month'] = monthly_summary['Month'].astype(str)
            monthly_summary.to_excel(writer, sheet_name='Monthly Summary', index=False)
            
            # Formats can be applied here using xlsxwriter if needed
        print(f"Saved Excel report to {excel_filename}.\n")
    except Exception as e:
         print(f"Error saving Excel report: {e}")

def run_pipeline():
    """Main function to run the full automation script."""
    print("=== Data Cleaning & Reporting Pipeline Started ===\n")
    
    # 1. Load Data
    df = load_data()
    if df is None:
        return
        
    # 2. Clean Data
    df_clean = clean_data(df)
    
    # 3. Generate Insights
    generate_insights(df_clean)
    
    # 4. Create Reports
    create_report(df_clean)
    
    print("=== Pipeline Execution Complete ===")

if __name__ == "__main__":
    run_pipeline()
