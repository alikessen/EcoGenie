from modules.carbon_data import carbon_data

def getDietData():
    """Collects user input for diet habits and returns a structured dictionary."""
    print("Diet Details:\n")

    while True:
        diet_type = input("Are you vegan, vegetarian, or neither? (vegan/vegetarian/neither): ").strip().lower()
        if diet_type in ["vegan", "vegetarian", "neither"]:
            break
        print("Invalid input. Please type 'vegan', 'vegetarian', or 'neither'.")

    if diet_type == "vegan":
        while True:
            try:
                vegan_meals_per_week = int(input("How many vegan meals do you eat per week? (0 to 21): ").strip())
                if 0 <= vegan_meals_per_week <= 21:
                    break
                print("Invalid input. Please enter a number between 0 and 21.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        return {
            "diet_type": "vegan",
            "vegan_meals_per_week": vegan_meals_per_week,
            "beef_per_kg": 0,
            "chicken_per_kg": 0,
            "fish_per_kg": 0,
            "milk_liters_per_week": 0,
            "eggs_per_week": 0,
        }

    elif diet_type == "vegetarian":
        while True:
            try:
                milk_liters_per_week = float(input("How many liters of milk do you consume per week? (0 to 10): ").strip())
                if 0 <= milk_liters_per_week <= 10:
                    break
                print("Invalid input. Please enter a number between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            try:
                eggs_per_week = int(input("How many eggs do you eat per week? (0 to 21): ").strip())
                if 0 <= eggs_per_week <= 21:
                    break
                print("Invalid input. Please enter a number between 0 and 21.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        return {
            "diet_type": "vegetarian",
            "vegan_meals_per_week": 0,
            "beef_per_kg": 0,
            "chicken_per_kg": 0,
            "fish_per_kg": 0,
            "milk_liters_per_week": milk_liters_per_week,
            "eggs_per_week": eggs_per_week,
        }

    elif diet_type == "neither":
        while True:
            try:
                beef_per_kg = float(input("How many kilograms of beef do you consume in a week? (0 to 10): ").strip())
                if 0 <= beef_per_kg <= 10:
                    break
                print("Invalid input. Please enter a number between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            try:
                chicken_per_kg = float(input("How many kilograms of chicken do you consume in a week? (0 to 10): ").strip())
                if 0 <= chicken_per_kg <= 10:
                    break
                print("Invalid input. Please enter a number between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            try:
                fish_per_kg = float(input("How many kilograms of fish/seafood do you consume in a week? (0 to 10): ").strip())
                if 0 <= fish_per_kg <= 10:
                    break
                print("Invalid input. Please enter a number between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            try:
                vegetarian_meals_per_week = int(input("How many of your meals are vegetarian or vegan per week? (0 to 21): ").strip())
                if 0 <= vegetarian_meals_per_week <= 21:
                    break
                print("Invalid input. Please enter a number between 0 and 21.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            try:
                milk_liters_per_week = float(input("How many liters of milk do you consume per week? (0 to 10): ").strip())
                if 0 <= milk_liters_per_week <= 10:
                    break
                print("Invalid input. Please enter a number between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            try:
                eggs_per_week = int(input("How many eggs do you eat per week? (0 to 21): ").strip())
                if 0 <= eggs_per_week <= 21:
                    break
                print("Invalid input. Please enter a number between 0 and 21.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        return {
            "diet_type": "neither",
            "vegan_meals_per_week": vegetarian_meals_per_week,
            "beef_per_kg": beef_per_kg,
            "chicken_per_kg": chicken_per_kg,
            "fish_per_kg": fish_per_kg,
            "milk_liters_per_week": milk_liters_per_week,
            "eggs_per_week": eggs_per_week,
        }

def calculateDietFootprint(diet_data):
    """Calculates the diet-related carbon footprint using values from CSV."""
    footprint = 0.0

    # Retrieve emission factors dynamically from CSV data
    footprint += diet_data["beef_per_kg"] * carbon_data["diet"]["beef"]
    footprint += diet_data["chicken_per_kg"] * carbon_data["diet"]["chicken"]
    footprint += diet_data["fish_per_kg"] * carbon_data["diet"]["fish"]
    footprint += diet_data["milk_liters_per_week"] * carbon_data["diet"].get("milk", 1.25)  # Default factor if missing
    footprint += diet_data["eggs_per_week"] * carbon_data["diet"].get("eggs", 2.2 / 12)  # Per egg factor

    return footprint

# Debugging: Run a test case when executing this script directly
if __name__ == "__main__":
    sample_diet = {
        "beef_per_kg": 2.0,
        "chicken_per_kg": 1.5,
        "fish_per_kg": 1.0,
        "milk_liters_per_week": 3,
        "eggs_per_week": 6
    }
    print("Diet Carbon Footprint:", calculateDietFootprint(sample_diet))
