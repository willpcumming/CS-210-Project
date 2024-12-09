EMS Inventory Management System
This project is a data-driven inventory management system designed specifically for Emergency Medical Services (EMS) agencies. It uses simulated inventory data to identify trends, analyze usage, and provide insights into restocking and critical stock levels.

Setup Instructions
1. Generate the Dataset
The dataset simulates monthly supply levels for critical EMS items like Bandages, Oxygen Tanks, IV Kits, and more.

The dataset will be automatically generated as ambulance_items_usage.csv when you run the script.
2. Creating the Virtual Environment
To isolate project dependencies, create a virtual environment:

bash
Copy code
python -m venv venv
3. Activating the Virtual Environment
Activate the virtual environment with the following command:

Linux/Mac:
bash
Copy code
source ./venv/bin/activate
Windows:
bash
Copy code
.\venv\Scripts\activate
4. Installing Required Libraries
Install all necessary libraries by running:

bash
Copy code
pip install -r requirements.txt
5. Running the Project
To execute the project and analyze the data, simply run the main script:

bash
Copy code
python main.py
This script will:

Generate the dataset.
Create an SQLite database to store the data.
Preprocess the data to clean it and calculate monthly usage.
Analyze trends in inventory usage.
Provide insights into restocking patterns and critical stock levels.
Repository Structure
generate_dataset.py: Generates the simulated EMS inventory dataset.
main.py: Main script to orchestrate the data processing and analysis workflow.
ambulance_items_usage.csv: The generated dataset (created when the script is run).
ems_inventory.db: SQLite database containing raw and processed data.
requirements.txt: List of required libraries and dependencies.
README.md: Instructions and documentation for setting up and running the project.
Future Enhancements
Integration of real-world EMS inventory data.
Implementation of predictive analytics using machine learning.
Development of a user-friendly interface for easier interaction with the system.
