import pandas as pd
import numpy as np

def generate_dataset(output_file="ambulance_items_usage.csv"):
    """
    Generates a dataset simulating EMS inventory usage and saves it as a CSV file.

    Args:
        output_file (str): The name of the CSV file to save the dataset.

    Returns:
        None
    """
    # Define parameters
    items = [
        "Bandages",
        "Oxygen Tanks",
        "IV Kits",
        "Defibrillator Pads",
        "Gloves",
        "Syringes",
        "Splints",
        "Medications",
    ]
    start_year = 2014
    end_year = 2023
    max_values = {
        "Bandages": 500,
        "Oxygen Tanks": 20,
        "IV Kits": 100,
        "Defibrillator Pads": 50,
        "Gloves": 1000,
        "Syringes": 500,
        "Splints": 200,
        "Medications": 300,
    }
    restock_probability = 0.1  # Probability of restocking each month

    # Generate months and years
    months = [f"{year}-{month:02d}" for year in range(start_year, end_year + 1) for month in range(1, 13)]

    # Initialize dataset
    data = {item: [] for item in items}
    data["Month"] = []

    # Generate supply levels
    for month in months:
        data["Month"].append(month)
        for item in items:
            max_supply = max_values[item]
            if len(data[item]) == 0:
                current_supply = max_supply  # Start each item at max supply
            else:
                current_supply = data[item][-1]  # Get last month's supply
            # Decrease supply by a random amount
            decrease = np.random.randint(1, max_supply // 5)
            current_supply -= decrease
            # Restock randomly
            if np.random.random() < restock_probability or current_supply < 0:
                current_supply = max_supply
            # Ensure supply isn't negative
            current_supply = max(0, current_supply)
            data[item].append(current_supply)

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Dataset successfully created and saved as '{output_file}'.")