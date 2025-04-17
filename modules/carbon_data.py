import csv
import os

 #Load CO2 emission data from CSV and return it as a dictionary
def load_carbon_data():
   
    carbon_data = {}
    csv_path = os.path.join(os.path.dirname(__file__), "../data/carbon_data.csv")

    with open(csv_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = row["category"]
            item = row["item"]
            co2_per_unit = float(row["co2_per_unit"])

            # Store data in a nested dictionary
            if category not in carbon_data:
                carbon_data[category] = {}
            carbon_data[category][item] = co2_per_unit

    return carbon_data

# Load the data at startup
carbon_data = load_carbon_data()

# Print loaded data when running this file
if __name__ == "__main__":
    print(carbon_data)
