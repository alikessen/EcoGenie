def getEnergyData():
    print("Energy Consumption Details:\n")

    while True:
        try:
            electricity_kwh_per_month = float(input("How many kilowatt-hours (kWh) of electricity do you use per month? ").strip())
            if electricity_kwh_per_month >= 0:
                break
            print("Invalid input. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    while True:
        electricity_source = input("Is your electricity sourced from renewables? (yes/no/some): ").strip().lower()
        if electricity_source in ["yes", "no", "some"]:
            break
        print("Invalid input. Please type 'yes', 'no', or 'some'.")

    while True:
        heating_type = input("What type of heating system do you use? (gas/electric/oil/none): ").strip().lower()
        if heating_type in ["gas", "electric", "oil", "none"]:
            break
        print("Invalid input. Please type 'gas', 'electric', 'oil', or 'none'.")

    gas_usage_cubic_meters = 0
    if heating_type == "gas":
        while True:
            try:
                gas_usage_cubic_meters = float(input("How many cubic meters of gas do you use per month? ").strip())
                if gas_usage_cubic_meters >= 0:
                    break
                print("Invalid input. Please enter a positive number.")
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
    # Carbon emission factors
    carbon_data = {
        "electricity": {
            "non_renewable": 0.5,  # kg CO2 per kWh
            "renewable": 0.0,      # kg CO2 per kWh
            "mixed": 0.25,         # kg CO2 per kWh (
        },
        "heating": {
            "gas": 1.9,    # kg CO2 per cubic meter of gas
            "oil": 2.9,    # kg CO2 per liter of oil
        }
    }

    # Initialize footprint
    footprint = 0.0

    # Electricity footprint
    if energy_data["electricity_source"] == "yes":
        footprint += energy_data["electricity_kwh_per_month"] * carbon_data["electricity"]["renewable"]
    elif energy_data["electricity_source"] == "no":
        footprint += energy_data["electricity_kwh_per_month"] * carbon_data["electricity"]["non_renewable"]
    elif energy_data["electricity_source"] == "some":
        footprint += energy_data["electricity_kwh_per_month"] * carbon_data["electricity"]["mixed"]

    # Heating footprint
    if energy_data["heating_type"] == "gas":
        footprint += energy_data["gas_usage_cubic_meters"] * carbon_data["heating"]["gas"]
    elif energy_data["heating_type"] == "oil":
        oil_usage_liters = energy_data["gas_usage_cubic_meters"]  
        footprint += oil_usage_liters * carbon_data["heating"]["oil"]


    footprint = footprint / 4  # Convert from monthly to weekly
    return footprint
    