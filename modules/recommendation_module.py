from modules.carbon_data import carbon_data


def generateLogicalRecommendations(transportation_data, diet_data, energy_data, user_footprints):
    recommendations = []

    # --- Transport: Work travel ---
    mode_of_transport = transportation_data.get("work_mode", "")
    distance_to_work = transportation_data.get("work_distance_km", 0)
    work_days = transportation_data.get("work_days", 0)
    work_car_type = transportation_data.get("work_car_type", "")
    work_pt_type = transportation_data.get("work_public_transport_type", "")
    transport_footprint = user_footprints.get("transportation", 0)

    if mode_of_transport == "car":
        if distance_to_work <= 5:
            savings = transport_footprint * 0.15
            recommendations.append(("Consider walking or cycling to work if your commute is short.", savings))
        else:
            savings = transport_footprint * 0.7
            recommendations.append(("Switch to public transport for long commutes to reduce emissions.", savings))

        if work_car_type in ["petrol", "diesel"]:
            savings = transport_footprint * 0.2
            recommendations.append(("Switch to electric or hybrid vehicles, or carpool when possible.", savings))

    elif mode_of_transport == "public transport" and work_pt_type == "bus":
        savings = transport_footprint * 0.15
        recommendations.append(("Try using the tube instead of the bus for faster and cleaner commutes.", savings))

    # --- Transport: Leisure travel ---
    leisure_mode = transportation_data.get("leisure_mode", "")
    leisure_distance = transportation_data.get("leisure_distance", 0)
    leisure_days = transportation_data.get("leisure_days", 0)
    leisure_type = transportation_data.get("leisure_type", "")

    if leisure_mode == "car" and leisure_type in ["petrol", "diesel"]:
        savings = leisure_distance * leisure_days * 0.3  # example value
        recommendations.append(("Reduce leisure car travel or switch to electric options.", savings))

    if leisure_mode == "public transport" and leisure_type == "bus":
        savings = leisure_distance * leisure_days * 0.2
        recommendations.append(("Use tube instead of bus for lower emissions.", savings))

    # Diet Recommendations
    if diet_data.get("beef_per_kg", 0) > 1.5:
        beef_emission = carbon_data["diet"]["beef"]
        beef_savings = (diet_data["beef_per_kg"] * 0.5) * beef_emission
        recommendations.append(("Reduce your beef consumption by 50% per week.", beef_savings))

    if diet_data.get("chicken_per_kg", 0) > 1:
        chicken_emission = carbon_data["diet"]["chicken"]
        chicken_savings = (diet_data["chicken_per_kg"] * 0.5) * chicken_emission
        recommendations.append(("Reduce your chicken consumption by 50% per week.", chicken_savings))

    if diet_data.get("fish_per_kg", 0) > 1:
        fish_emission = carbon_data["diet"]["fish"]
        fish_savings = (diet_data["fish_per_kg"] * 0.5) * fish_emission
        recommendations.append(("Reduce your fish consumption by 50% per week.", fish_savings))

    if diet_data.get("milk_liters_per_week", 0) > 2:
        milk_emission = carbon_data["diet"]["milk"]
        milk_savings = (diet_data["milk_liters_per_week"] * 0.5) * milk_emission
        recommendations.append(("Reduce your milk consumption by 50% per week.", milk_savings))

    if diet_data.get("eggs_per_week", 0) > 3:
        egg_emission = carbon_data["diet"]["eggs"]
        egg_savings = 2 * egg_emission  
        recommendations.append(("Reduce your egg consumption by 2 per week.", egg_savings))

    if diet_data.get("vegan_meals_per_week", 0) < 4:
        avg_meal_emission = carbon_data["diet"]["average_meal"]
        vegan_meal_emission = carbon_data["diet"]["vegan_meals"]
        co2_saved_per_meal = avg_meal_emission - vegan_meal_emission
        vegan_savings = co2_saved_per_meal * (4 - diet_data["vegan_meals_per_week"])

        recommendations.append(("Try making your breakfasts plant-based at least 4 times per week.", vegan_savings))

    elif 4 <= diet_data["vegan_meals_per_week"] < 10:
        avg_meal_emission = carbon_data["diet"]["average_meal"]
        vegan_meal_emission = carbon_data["diet"]["vegan_meals"]
        co2_saved_per_meal = avg_meal_emission - vegan_meal_emission
        needed_meals = 10 - diet_data["vegan_meals_per_week"]
        vegan_savings = co2_saved_per_meal * needed_meals

        recommendations.append((f"Try increasing your plant-based meals by {needed_meals} more per week.", vegan_savings))

    # Energy Recommendations
    electricity_source = energy_data.get("electricity_source", "")
    if electricity_source == "no":
        electricity_savings = user_footprints.get("energy", 0)  # Savings equal to electricity footprint if switching to renewables
        recommendations.append(("Switch to a renewable energy provider.", electricity_savings))
    elif electricity_source == "some":
        electricity_savings2 = user_footprints.get("energy", 0) / 2  # Savings equal to electricity footprint if switching to renewables
        recommendations.append(("Switch to a fully renewable energy provider.", electricity_savings2))

    if energy_data.get("gas_usage_cubic_meters", 0) > 50:
        gas_savings = user_footprints.get("energy", 0) * 0.1  # Assume 10% savings for reducing gas usage
        recommendations.append(("Reduce gas heating usage by 10%.", gas_savings))

    if energy_data.get("energy_efficient_appliances", "") == "no":
        appliance_savings = 10  # Fixed savings for upgrading appliances
        recommendations.append(("Upgrade to energy-efficient appliances or install LED bulbs.", appliance_savings))

    # Rank Recommendations by CO2 Savings
    ranked_recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

    # Return Top 3 Recommendations
    return ranked_recommendations[:3]
