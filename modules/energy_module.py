from modules.carbon_data import carbon_data

def getEnergyData():
    """Collects user input for energy consumption and returns a structured dictionary."""
    try:
        print("Energy Consumption Details:\n")
    except KeyError as e:
        raise ValueError(f"Missing CO₂ data for: {e}")

    while True:
        try:
            electricity_kwh_per_month = float(input("How many kilowatt-hours (kWh) of electricity do you use per month? (0-2000): ").strip())
            if 0 <= electricity_kwh_per_month <= 2000:
                break
            print("Invalid input. Please enter a number between 0 and 2000.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    while True:
        electricity_source = input("Is your electricity from renewable sources? (yes/no/some): ").strip().lower()
        if electricity_source in ["yes", "no", "some"]:
            break
        print("Invalid input. Please type 'yes', 'no', or 'some'.")

    while True:
        heating_type = input("What type of heating do you use? (gas/electric/oil/none): ").strip().lower()
        if heating_type in ["gas", "electric", "oil", "none"]:
            break
        print("Invalid input. Please type 'gas', 'electric', 'oil', or 'none'.")

    gas_usage_cubic_meters = 0  # Default
    if heating_type == "gas":
        while True:
            try:
                gas_usage_cubic_meters = float(input("How many cubic meters of gas do you use per month? (0-500): ").strip())
                if 0 <= gas_usage_cubic_meters <= 500:
                    break
                print("Invalid input. Please enter a number between 0 and 500.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    while True:
        energy_efficient_appliances = input("Do you use energy-efficient appliances? (yes/no/some): ").strip().lower()
        if energy_efficient_appliances in ["yes", "no", "some"]:
            break
        print("Invalid input. Please type 'yes', 'no', or 'some'.")

    return {
        "electricity_kwh_per_month": electricity_kwh_per_month,
        "electricity_source": electricity_source,
        "heating_type": heating_type,
        "gas_usage_cubic_meters": gas_usage_cubic_meters,
        "energy_efficient_appliances": energy_efficient_appliances,
    }

def calculateEnergyFootprint(energy_data):
    """Calculates the energy-related carbon footprint using values from CSV."""
    try:
        footprint = 0.0
    except KeyError as e:
        raise ValueError(f"Missing CO₂ data for: {e}")

    # Electricity emissions based on source
    electricity_source = energy_data["electricity_source"]
    electricity_factor = carbon_data["energy"].get(f"electricity_{electricity_source}", 0.5)  # Default 0.5 kg CO2/kWh

    footprint += energy_data["electricity_kwh_per_month"] * electricity_factor

    # Heating type
    if energy_data["heating_type"] == "gas":
        footprint += energy_data["gas_usage_cubic_meters"] * carbon_data["energy"].get("gas", 2.0)  # Default 2.0 kg CO2/m³

    elif energy_data["heating_type"] == "oil":
        footprint += energy_data["electricity_kwh_per_month"] * carbon_data["energy"].get("oil", 0.32)  

    # Appliance savings: Reduce footprint if using energy-efficient appliances
    if energy_data["energy_efficient_appliances"] == "yes":
        footprint *= 0.85  # 15% savings for efficient appliances
    elif energy_data["energy_efficient_appliances"] == "some":
        footprint *= 0.90  # 10% savings

    return footprint / 4  # Convert from monthly to weekly footprint

if __name__ == "__main__":
    sample_energy = {
        "electricity_kwh_per_month": 350,
        "electricity_source": "mixed",
        "heating_type": "gas",
        "gas_usage_cubic_meters": 50,
        "energy_efficient_appliances": "yes"
    }
    print("Energy Carbon Footprint:", calculateEnergyFootprint(sample_energy))