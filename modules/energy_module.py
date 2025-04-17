from modules.carbon_data import carbon_data

# Calculates the energy related carbon footprint using values from CSV
def calculateEnergyFootprint(energy_data):
    
    try:
        footprint = 0.0

        # Electricity emissions based on source
        electricity_source = energy_data["electricity_source"]
        electricity_factor = carbon_data["energy"].get(f"electricity_{electricity_source}", 0.5)  # Default 0.5 kg CO2/kWh

        footprint += energy_data["electricity_kwh_per_month"] * electricity_factor

        # Heating type
        if energy_data["heating_type"] == "gas":
            footprint += energy_data["gas_usage_cubic_meters"] * carbon_data["energy"].get("gas", 2.0)  # Default 2.0 kg CO2/m3

        elif energy_data["heating_type"] == "oil":
            footprint += energy_data["electricity_kwh_per_month"] * carbon_data["energy"].get("oil", 0.32)  

        # Appliance savings: Reduce footprint if using energy efficient appliances
        if energy_data["energy_efficient_appliances"] == "yes":
            footprint *= 0.85  # 15% savings for efficient appliances
        elif energy_data["energy_efficient_appliances"] == "some":
            footprint *= 0.90  # 10% savings

        return footprint / 4  # Convert from monthly to weekly footprint

    except KeyError as e:
            raise ValueError(f"Missing CO2 data for: {e}")

if __name__ == "__main__":
    sample_energy = {
        "electricity_kwh_per_month": 350,
        "electricity_source": "mixed",
        "heating_type": "gas",
        "gas_usage_cubic_meters": 50,
        "energy_efficient_appliances": "yes"
    }
    print("Energy Carbon Footprint:", calculateEnergyFootprint(sample_energy))