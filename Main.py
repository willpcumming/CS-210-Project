from generate_dataset import generate_dataset
import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def create_database_and_load_csv(db_name="ems_inventory.db", csv_file="ambulance_items_usage.csv"):
    """
    Creates a SQLite database and loads a CSV file into it.

    Args:
        db_name (str): Name of the SQLite database file.
        csv_file (str): Path to the CSV file to load.

    Returns:
        None
    """
    try:
        # Load CSV into DataFrame
        df = pd.read_csv(csv_file)
        print(f"CSV file '{csv_file}' loaded successfully.")

        # Create SQLite database and save the DataFrame
        conn = sqlite3.connect(db_name)
        df.to_sql("inventory", conn, if_exists="replace", index=False)
        print(f"Data loaded into database '{db_name}' in table 'inventory'.")

        # Close the connection
        conn.close()
    except FileNotFoundError:
        print(f"File '{csv_file}' not found. Ensure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def verify_database(db_name="ems_inventory.db"):
    """
    Verifies the contents of the database by querying the first 5 rows.

    Args:
        db_name (str): Name of the SQLite database file.

    Returns:
        None
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)

        # Query the inventory table
        query = "SELECT * FROM inventory LIMIT 5"
        df = pd.read_sql_query(query, conn)
        print("Sample data from the database:")
        print(df)

        # Close the connection
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def preprocess_data(data, max_inventory):
    """
    Cleans and preprocesses the EMS inventory data and calculates monthly usage.

    Args:
        data (DataFrame): Raw data loaded from the database.
        max_inventory (dict): A dictionary containing max inventory levels for each item.

    Returns:
        DataFrame: Preprocessed data with additional features, including usage.
    """
    # Handle missing values
    data = data.dropna()
    print("Missing values removed.")

    # Remove duplicates
    data = data.drop_duplicates()
    print("Duplicates removed.")

    # Clean outliers
    for col in data.select_dtypes(include=[np.number]).columns:
        mean = data[col].mean()
        std = data[col].std()
        data = data[(data[col] >= mean - 3 * std) & (data[col] <= mean + 3 * std)]
    print("Outliers cleaned.")

    # Standardize formats
    if 'Month' in data.columns:
        data['Month'] = pd.to_datetime(data['Month'])
        data = data.sort_values(by='Month')
    print("Date formats standardized.")

    # Calculate monthly usage
    for col in data.select_dtypes(include=[np.number]).columns:
        if col != "Month":  # Skip non-numeric or non-inventory columns
            usage = data[col].diff() * -1  # Calculate usage as the negative difference
            restocks = data[col].diff() > 0  # Detect restocks where inventory increases
            usage[restocks] = 0  # Ignore restock months in usage calculation
            usage[data[col] == max_inventory.get(col, float('inf'))] = 0  # Ignore maxed-out months
            data[f"{col}_Usage"] = usage.fillna(0)  # Add usage column and handle NaN
    print("Monthly usage calculated.")

    # Drop rows with NaN values introduced by rolling or lag operations
    data = data.dropna()
    print("Rows with NaN values dropped.")

    print("Data preprocessing completed.")
    return data


def preprocess_and_save(db_name="ems_inventory.db"):
    """
    Extracts data from the database, preprocesses it, and saves the cleaned version back.

    Args:
        db_name (str): SQLite database name.

    Returns:
        DataFrame: Preprocessed data.
    """
    try:
        # Load data from the database
        conn = sqlite3.connect(db_name)
        raw_data = pd.read_sql_query("SELECT * FROM inventory", conn)
        print("Data loaded from database.")

        # Define max inventory levels for each item
        max_inventory = {
            "Bandages": 500,
            "Oxygen Tanks": 20,
            "IV Kits": 100,
            "Defibrillator Pads": 50,
            "Gloves": 1000,
            "Syringes": 500,
            "Splints": 200,
            "Medications": 300,
        }

        # Preprocess the data
        processed_data = preprocess_data(raw_data, max_inventory)

        # Save preprocessed data back to the database
        processed_data.to_sql("preprocessed_inventory", conn, if_exists="replace", index=False)
        print("Preprocessed data saved to the database in 'preprocessed_inventory' table.")

        # Close the connection
        conn.close()
        return processed_data
    except Exception as e:
        print(f"An error occurred during preprocessing: {e}")
        return None



def analyze_trends(db_name="ems_inventory.db", smoothing_window=3):
    """
    Analyzes and visualizes trends in the preprocessed inventory usage data,
    plotting each item on a separate chart with optional data smoothing.

    Args:
        db_name (str): SQLite database name.
        smoothing_window (int): Window size for moving average smoothing.

    Returns:
        None
    """
    try:
        # Connect to the database and load preprocessed data
        conn = sqlite3.connect(db_name)
        data = pd.read_sql_query("SELECT * FROM preprocessed_inventory", conn)
        conn.close()

        # Ensure 'Month' is in datetime format
        data['Month'] = pd.to_datetime(data['Month'])

        # Select only usage columns
        usage_columns = [col for col in data.columns if '_Usage' in col]

        if not usage_columns:
            print("No usage data found for plotting.")
            return

        # Plot each usage column on a separate chart
        for col in usage_columns:
            plt.figure(figsize=(10, 5))

            # Apply smoothing using a rolling mean
            smoothed = data[col].rolling(window=smoothing_window).mean()

            # Plot raw and smoothed data
            plt.plot(data['Month'], data[col], label="Raw Data", alpha=0.5, color="blue", linestyle="--")
            plt.plot(data['Month'], smoothed, label=f"Smoothed (Window={smoothing_window})", color="red")

            plt.title(f"Usage Trends for {col.replace('_Usage', '')}")
            plt.xlabel("Month")
            plt.ylabel("Usage")
            plt.legend(title="Legend")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"An error occurred during trend analysis: {e}")

def analyze_restock_and_critical_stock(data, max_inventory):
    """
    Analyzes restocking patterns and critical stock levels for each inventory item.

    Args:
        data (DataFrame): Preprocessed inventory data.
        max_inventory (dict): A dictionary containing max inventory levels for each item.

    Returns:
        None
    """
    print("=== Restock and Critical Stock Analysis ===")

    for item, max_val in max_inventory.items():
        if item not in data.columns:
            print(f"Skipping {item}, not found in data.")
            continue

        print(f"\nAnalyzing {item}...")

        # Detect restocks: inventory increases where the previous value is below 20% of the max
        restocks = (data[item].diff() > 0) & (data[item].shift(1) < 0.2 * max_val)
        restock_dates = data['Month'][restocks]
        if not restock_dates.empty:
            print(f"Restocks occurred when inventory was below 20% of max ({0.2 * max_val}):")
            for date in restock_dates:
                print(f" - {date.strftime('%Y-%m')}")
        else:
            print("No restocks detected below critical levels.")

        # Detect critical stock levels: inventory drops below the maximum usage in any month
        usage_col = f"{item}_Usage"
        if usage_col in data.columns:
            max_usage = data[usage_col].max()
            critical_stock = data[item] < max_usage
            critical_dates = data['Month'][critical_stock]
            if not critical_dates.empty:
                print(f"Months when {item} stock fell below max usage ({max_usage}):")
                for date in critical_dates:
                    print(f" - {date.strftime('%Y-%m')}")
            else:
                print("No critical stock issues detected.")
        else:
            print(f"No usage data available for {item}.")

    print("\nAnalysis completed.")




if __name__ == "__main__":
    # Step 0: Generate the dataset
    print("Generating dataset...")
    dataset_file = "ambulance_items_usage.csv"
    generate_dataset(dataset_file)
    print(f"Dataset generated and saved as {dataset_file}.")

    # Step 1: Create the database and load the CSV
    create_database_and_load_csv()

    # Step 2: Verify the database contents
    verify_database()

    # Step 3: Preprocess the data and save it back to the database
    preprocessed_data = preprocess_and_save()

    # Step 4: Display a sample of the preprocessed data
    if preprocessed_data is not None:
        print(preprocessed_data.head(10))

    # Step 5: Analyze trends in the preprocessed data
    analyze_trends()

    # Step 6: Perform restock and critical stock analysis
    max_inventory = {
        "Bandages": 500,
        "Oxygen Tanks": 20,
        "IV Kits": 100,
        "Defibrillator Pads": 50,
        "Gloves": 1000,
        "Syringes": 500,
        "Splints": 200,
        "Medications": 300,
    }
    analyze_restock_and_critical_stock(preprocessed_data, max_inventory)