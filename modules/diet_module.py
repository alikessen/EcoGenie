from modules.carbon_data import carbon_data


def calculate_diet_footprint(diet_data):
    try:
        footprint = 0.0
        footprint += diet_data["beef_per_kg"] * carbon_data["diet"]["beef"]
        footprint += diet_data["chicken_per_kg"] * carbon_data["diet"]["chicken"]
        footprint += diet_data["fish_per_kg"] * carbon_data["diet"]["fish"]
        footprint += diet_data["milk_liters_per_week"] * carbon_data["diet"]["milk"]
        footprint += diet_data["eggs_per_week"] * carbon_data["diet"]["eggs"]
        footprint += diet_data["vegan_meals_per_week"] * carbon_data["diet"]["vegan_meals"]
        return footprint
    except KeyError as exc:
        raise ValueError(f"Missing CO2 data for: {exc}")


# Backward-compatible alias.
def calculateDietFootprint(diet_data):
    return calculate_diet_footprint(diet_data)


if __name__ == "__main__":
    sample_diet = {
        "beef_per_kg": 2.0,
        "chicken_per_kg": 1.5,
        "fish_per_kg": 1.0,
        "milk_liters_per_week": 3,
        "eggs_per_week": 6,
        "vegan_meals_per_week": 0,
    }
    print("Diet Carbon Footprint:", calculate_diet_footprint(sample_diet))
