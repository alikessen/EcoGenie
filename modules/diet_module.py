from modules.carbon_data import carbon_data

#Calculates the weekly carbon footprint of a user's diet using emission factors
def calculateDietFootprint(diet_data):
    try:
        footprint = 0.0
        footprint += diet_data["beef_per_kg"] * carbon_data["diet"]["beef"]
        footprint += diet_data["chicken_per_kg"] * carbon_data["diet"]["chicken"]
        footprint += diet_data["fish_per_kg"] * carbon_data["diet"]["fish"]
        footprint += diet_data["milk_liters_per_week"] * carbon_data["diet"]["milk"]
        footprint += diet_data["eggs_per_week"] * carbon_data["diet"]["eggs"]
        footprint += diet_data["vegan_meals_per_week"] * carbon_data["diet"]["vegan_meals"]
        return footprint

    except KeyError as e:
        raise ValueError(f"Missing CO₂ data for: {e}")


# Run a test case when executing this script directly
if __name__ == "__main__":
    sample_diet = {
        "beef_per_kg": 2.0,
        "chicken_per_kg": 1.5,
        "fish_per_kg": 1.0,
        "milk_liters_per_week": 3,
        "eggs_per_week": 6
    }
    print("Diet Carbon Footprint:", calculateDietFootprint(sample_diet))
