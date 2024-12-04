import pandas as pd
import numpy as np

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
data = {"Item": items}
for month in months:
    data[month] = []

# Generate supply levels
for item in items:
    max_supply = max_values[item]
    current_supply = max_supply  # Start each item at max supply
    supplies = []
    
    for month in months:
        # Decrease supply by a random amount
        decrease = np.random.randint(1, max_supply // 10)
        current_supply -= decrease
        
        # Restock randomly
        if np.random.random() < restock_probability or current_supply < 0:
            current_supply = max_supply
        
        # Ensure supply isn't negative
        current_supply = max(0, current_supply)
        supplies.append(current_supply)
    
    data["Item"].append(item)
    for i, month in enumerate(months):
        data[month].append(supplies[i])

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("ambulance_items_usage.csv", index=False)

print("Dataset created and saved as 'ambulance_items_usage.csv'.")
