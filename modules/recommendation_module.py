from modules.carbon_data import carbon_data

# Generates personalized sustainability recommendations based on a user's lifestyle data in transportation, diet, and energy use.
def generateLogicalRecommendations(transportation_data, diet_data, energy_data, user_footprints):
    recommendations = []

    # ---------------------------------------
    # Transportation Recommendations
    # ---------------------------------------

    # Transport: Work travel
    mode_of_transport = transportation_data.get("work_mode", "")
    distance_to_work = transportation_data.get("work_distance_km", 0)
    work_days = transportation_data.get("work_days", 0)
    work_car_type = transportation_data.get("work_car_type", "")
    work_pt_type = transportation_data.get("work_pt_type", "")
    total_distance_work = work_days * distance_to_work * 2

    if mode_of_transport == "car":
        emission_factor = carbon_data["transport"][f"car_{work_car_type}"]
        if distance_to_work <= 5:
            savings = total_distance_work * emission_factor
            recommendations.append(("Consider walking or cycling to work.", savings))
        elif distance_to_work > 5 and work_car_type != "electric":
            savings = (total_distance_work * emission_factor) - (
                total_distance_work * carbon_data["transport"]["both"]
            )
            recommendations.append(
                ("Switch to public transport for long commutes to reduce emissions.", savings)
            )
    elif mode_of_transport == "public transport" and work_pt_type == "bus":
        savings = (total_distance_work * carbon_data["transport"]["bus"]) - (
            total_distance_work * carbon_data["transport"]["tube"]
        )
        recommendations.append(
            ("Switch from bus to tube if possible for faster and cleaner commutes.", savings)
        )

    leisure_mode = transportation_data.get("leisure_mode", "")
    leisure_distance = transportation_data.get("leisure_distance", 0)
    leisure_days = transportation_data.get("leisure_days", 0)
    leisure_type = transportation_data.get("leisure_type", "")
    total_distance_leisure = leisure_days * leisure_distance * 2 # Round trip

    if leisure_mode == "car":
        leisure_emission_factor = carbon_data["transport"].get(f"car_{leisure_type}", 0)
        if leisure_emission_factor > 0:
            savings = total_distance_leisure * leisure_emission_factor / 2
            recommendations.append(("Reduce leisure car travel by 50% per week.", savings))
    elif leisure_mode == "public transport" and leisure_type == "bus":
        bus_emission_factor = carbon_data["transport"].get("bus", 0)
        tube_emission_factor = carbon_data["transport"].get("tube", 0)
        savings = total_distance_leisure * (bus_emission_factor - tube_emission_factor)
        recommendations.append(
            ("Use the tube instead of the bus for lower emissions during leisure trips.", savings)
        )


    # ---------------------------------------
    # Diet Recommendations
    # ---------------------------------------

    if diet_data.get("beef_per_kg", 0) > 0.5:
        beef_emission = carbon_data["diet"]["beef"]
        beef_savings = (diet_data["beef_per_kg"] * 0.5) * beef_emission
        recommendations.append(("Reduce your beef consumption by 50% per week.", beef_savings))

    if diet_data.get("chicken_per_kg", 0) > 0.2:
        chicken_emission = carbon_data["diet"]["chicken"]
        chicken_savings = (diet_data["chicken_per_kg"] * 0.5) * chicken_emission
        recommendations.append(("Reduce your chicken consumption by 50% per week.", chicken_savings))

    if diet_data.get("fish_per_kg", 0) > 0.1:
        fish_emission = carbon_data["diet"]["fish"]
        fish_savings = (diet_data["fish_per_kg"] * 0.5) * fish_emission
        recommendations.append(("Reduce your fish consumption by 50% per week.", fish_savings))

    if diet_data.get("milk_liters_per_week", 0) > 0.5:
        milk_emission = carbon_data["diet"]["milk"]
        milk_savings = (diet_data["milk_liters_per_week"] * 0.5) * milk_emission
        recommendations.append(("Reduce your milk consumption by 50% per week.", milk_savings))

    eggs_per_week = diet_data.get("eggs_per_week", 0)
    if 3 < eggs_per_week < 7:
        egg_savings = 2 * carbon_data["diet"]["eggs"]
        recommendations.append(("Reduce your egg consumption by 2 per week.", egg_savings))
    elif eggs_per_week > 7:
        egg_savings = 3 * carbon_data["diet"]["eggs"]
        recommendations.append(("Reduce your egg consumption by 3 per week.", egg_savings))

    vegan_meals = diet_data.get("vegan_meals_per_week", 0)
    if vegan_meals < 5:
        avg_meal_emission = carbon_data["diet"]["average_meal"]
        vegan_meal_emission = carbon_data["diet"]["vegan_meals"]
        co2_saved_per_meal = avg_meal_emission - vegan_meal_emission
        vegan_savings = co2_saved_per_meal * (4 - vegan_meals)
        recommendations.append(
            ("Try making your breakfasts plant-based at least 4 times per week.", vegan_savings)
        )
    elif 5 <= vegan_meals < 10:
        avg_meal_emission = carbon_data["diet"]["average_meal"]
        vegan_meal_emission = carbon_data["diet"]["vegan_meals"]
        co2_saved_per_meal = avg_meal_emission - vegan_meal_emission
        needed_meals = 10 - vegan_meals
        vegan_savings = co2_saved_per_meal * needed_meals
        recommendations.append(
            (f"Try increasing your plant-based meals by {needed_meals} more per week.", vegan_savings)
        )

    electricity_source = energy_data.get("electricity_source", "")
    electricity_footprint = user_footprints.get("energy", 0)

    if electricity_source == "non_renewable":
        recommendations.append(
            ("Switch to a renewable energy provider to eliminate electricity emissions.", electricity_footprint)
        )
    elif electricity_source == "mixed":
        recommendations.append(
            (
                "Switch to a fully renewable energy provider to cut electricity emissions by 50%.",
                electricity_footprint * 0.5,
            )
        )

    gas_usage = energy_data.get("gas_usage_cubic_meters", 0)
    if gas_usage > 50:
        gas_footprint = gas_usage * carbon_data["energy"]["gas"]
        recommendations.append(("Reduce gas heating usage by 10%.", gas_footprint * 0.1))

    if energy_data.get("energy_efficient_appliances", "") == "no":
        appliance_savings = electricity_footprint * 0.15 * 0.3
        recommendations.append(
            ("Upgrade to energy-efficient appliances or install LED bulbs.", appliance_savings)
        )

    recommendations = [(text, saving) for text, saving in recommendations if saving > 0]
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:3]


# Backward-compatible alias.
def generateLogicalRecommendations(transportation_data, diet_data, energy_data, user_footprints):
    return generate_logical_recommendations(
        transportation_data,
        diet_data,
        energy_data,
        user_footprints,
    )
