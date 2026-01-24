import pandas as pd
import glob
import os

def load_and_merge_data(data_folder='data/'):
    # Find all CSV files in the data folder
    all_files = glob.glob(os.path.join(data_folder, "*.csv"))
    combined_list = []

    for file in all_files:
        # Get city name from the filename (e.g., 'Bangalore' from 'data/Bangalore.csv')
        city_name = os.path.basename(file).replace('.csv', '')
        
        df = pd.read_csv(file)
        # Add a column so the model knows which city the data belongs to
        df['City'] = city_name
        combined_list.append(df)
        print(f"Loaded {city_name} with {len(df)} rows.")

    # Combine all into one DataFrame
    full_df = pd.concat(combined_list, ignore_index=True)
    return full_df

def clean_data(df):
    # 1. Remove duplicates
    df = df.drop_duplicates()

    # 2. Handle missing values 
    # Replace 'No info' or '9' (often used in these datasets) with 0 or NaN
    # For now, we fill simple numeric NaNs with the median
    df['Area'] = pd.to_numeric(df['Area'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna(subset=['Price', 'Area']) # We can't predict without these

    return df

if __name__ == "__main__":
    raw_data = load_and_merge_data()
    cleaned_data = clean_data(raw_data)
    
    # Create a 'cleaned' folder or just save in data
    cleaned_data.to_csv('data/master_data.csv', index=False)
    print("Success! master_data.csv created in data/ folder.")