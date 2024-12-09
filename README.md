
# EMS Inventory Management System

## Setup Instructions

### 1. 1. Generate the Dataset
The dataset simulates monthly supply levels for critical EMS items like Bandages, Oxygen Tanks, IV Kits, and more. You do not need to download any files manually as the dataset will be automatically generated when you run the script.

---

### 2. Creating the Virtual Environment
To isolate project dependencies, create a virtual environment:

```bash
python -m venv venv
```

---

### 3. Activating the Virtual Environment
Activate the virtual environment with the following command:

- **Linux/Mac**:
  ```bash
  source ./venv/bin/activate
  ```

- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```

---

### 4. Installing Required Libraries
Install all necessary libraries by running:

```bash
pip install -r requirements.txt
```

---

### 5. Configuring the Python Code
To properly run the project:

```bash
python main.py
```
This script will:

1. Generate the dataset.
2. Create an SQLite database to store the data.
3. Preprocess the data to clean it and calculate monthly usage.
4. Analyze trends in inventory usage.
5. Provide insights into restocking patterns and critical stock levels.

---

### Repository Structure
**'generate_dataset.py'**: Script for generating the simulated EMS inventory dataset.
**'main.py'**: Main script to orchestrate the data processing and analysis workflow.
**'ambulance_items_usage.csv'**: The generated dataset (created when the script is run).
**'ems_inventory.db'**: SQLite database containing raw and processed data.
**'requirements.txt'**: List of required libraries and dependencies.
**'README.md'**: Instructions and documentation for setting up and running the project.

---
