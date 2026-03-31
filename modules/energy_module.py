from modules.carbon_data import carbon_data


VALID_SOURCES = {"renewable", "non_renewable", "mixed", ""}


def calculate_energy_footprint(energy_data):
    source = energy_data["electricity_source"]
    if source not in VALID_SOURCES:
        raise ValueError(f"Invalid electricity source: {source}")

    try:
        footprint = 0.0
        if source:
            electricity_factor = carbon_data["energy"][f"electricity_{source}"]
            footprint += energy_data["electricity_kwh_per_month"] * electricity_factor

        heating_type = energy_data["heating_type"]
        if heating_type == "gas":
            footprint += energy_data["gas_usage_cubic_meters"] * carbon_data["energy"]["gas"]
        elif heating_type == "oil":
            footprint += energy_data["electricity_kwh_per_month"] * carbon_data["energy"]["oil"]

        appliances = energy_data["energy_efficient_appliances"]
        if appliances == "yes":
            footprint *= 0.85
        elif appliances == "some":
            footprint *= 0.90

        return footprint / 4
    except KeyError as exc:
        raise ValueError(f"Missing CO2 data for: {exc}")


# Backward-compatible alias.
def calculateEnergyFootprint(energy_data):
    return calculate_energy_footprint(energy_data)


if __name__ == "__main__":
    sample_energy = {
        "electricity_kwh_per_month": 350,
        "electricity_source": "mixed",
        "heating_type": "gas",
        "gas_usage_cubic_meters": 50,
        "energy_efficient_appliances": "yes",
    }
    print("Energy Carbon Footprint:", calculate_energy_footprint(sample_energy))
