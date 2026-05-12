import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_messy_data(filename="raw_sales_data.csv", num_rows=100):
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    customers = [f"Customer_{i}" for i in range(1, 21)]
    products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Monitor", "Keyboard", "Mouse"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio"]
    
    data = []
    
    start_date = datetime(2023, 1, 1)
    
    for _ in range(num_rows):
        date = start_date + timedelta(days=random.randint(0, 365))
        customer = random.choice(customers)
        product = random.choice(products)
        quantity = random.randint(1, 10)
        price = round(random.uniform(20.0, 1500.0), 2)
        city = random.choice(cities)
        
        # Introduce "messiness"
        
        # 1. Missing values (10% chance)
        if random.random() < 0.1:
            quantity = np.nan
        if random.random() < 0.1:
            price = np.nan
        if random.random() < 0.1:
            city = np.nan
            
        # 2. Inconsistent text (20% chance)
        if pd.notna(city) and random.random() < 0.2:
            city = city.lower() + " "
        if random.random() < 0.2:
            product = " " + product.upper() + " "
            
        # 3. Wrong date formats (10% chance)
        date_str = date.strftime("%Y-%m-%d")
        if random.random() < 0.1:
            date_str = date.strftime("%d/%m/%Y") # mixed format
        if random.random() < 0.05:
            date_str = "invalid_date"
            
        data.append([date_str, customer, product, quantity, price, city])
        
    df = pd.DataFrame(data, columns=["Date", "Customer", "Product", "Quantity", "Price", "City"])
    
    # Introduce duplicate rows (5 duplicates)
    duplicates = df.sample(n=5, replace=True, random_state=1)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Shuffle the dataframe
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Generated messy dataset with {len(df)} rows and saved to '{filename}'.")

if __name__ == "__main__":
    generate_messy_data()
