def getDietData():
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
                chicken_per_kg = float(input("How many kilograms of chichken do you consume in a week? (0 to 10): ").strip())
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
            "vegan_meals_per_week": vegetarian_meals_per_week,  # Assuming plant-based meals are vegetarian/vegan
            "beef_per_kg": beef_per_kg,
            "chicken_per_kg": chicken_per_kg,
            "fish_per_kg": fish_per_kg,
            "milk_liters_per_week": milk_liters_per_week,
            "eggs_per_week": eggs_per_week,
        }


def calculateDietFootprint(diet_data):
    # Carbon emission factors (kg CO2 per unit)
    carbon_data = {
        "meat": {
            "beef": 40.0,      # kg CO2 per kg of beef
            "chicken": 8.0,    # kg CO2 per kg of chicken
            "fish": 4.0,       # kg CO2 per kg of fish/seafood
        },
        "dairy_and_eggs": {
            "milk": 1.25,       # kg CO2 per liter of milk
            "eggs": 2.2 / 12,  # kg CO2 per egg (4.8 per dozen eggs)
        },
        "plant_based": {
            "vegetarian_meal": 1.8,  # kg CO2 per vegetarian meal
            "vegan_meal": 1.9,       # kg CO2 per vegan meal
        }
    }

    # Initialize footprint
    footprint = 0.0

    # Calculate footprint based on diet type
    if diet_data["diet_type"] == "vegan":
        vegan_meals_per_week = diet_data["vegan_meals_per_week"]
        footprint += vegan_meals_per_week * carbon_data["plant_based"]["vegan_meal"]

    elif diet_data["diet_type"] == "vegetarian":
        milk_footprint = diet_data["milk_liters_per_week"] * carbon_data["dairy_and_eggs"]["milk"]
        eggs_footprint = diet_data["eggs_per_week"] * carbon_data["dairy_and_eggs"]["eggs"]
        vegetarian_footprint = diet_data["vegan_meals_per_week"] * carbon_data["plant_based"]["vegetarian_meal"]
        footprint += milk_footprint + eggs_footprint + vegetarian_footprint

    elif diet_data["diet_type"] == "neither":
        # Calculate meat footprints
        beef_footprint = diet_data["beef_per_kg"] * carbon_data["meat"]["beef"]
        chicken_footprint = diet_data["chicken_per_kg"] * carbon_data["meat"]["chicken"]
        fish_footprint = diet_data["fish_per_kg"] * carbon_data["meat"]["fish"]

        # Remaining meals are assumed to be vegetarian
        vegetarian_footprint = diet_data["vegan_meals_per_week"] * carbon_data["plant_based"]["vegetarian_meal"]

        # Calculate dairy and egg footprints
        milk_footprint = diet_data["milk_liters_per_week"] * carbon_data["dairy_and_eggs"]["milk"]
        eggs_footprint = diet_data["eggs_per_week"] * carbon_data["dairy_and_eggs"]["eggs"]

        # Sum up the total footprint
        footprint += (
            beef_footprint
            + chicken_footprint
            + fish_footprint
            + vegetarian_footprint
            + milk_footprint
            + eggs_footprint
        )

    return footprint