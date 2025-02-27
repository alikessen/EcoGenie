def generateLogicalRecommendations(transportation_data, diet_data, energy_data, user_footprints):
    recommendations = []

    # Prevent KeyError by using `.get()`
    mode_of_transport = transportation_data.get("mode_of_transport", "")
    distance_to_work = transportation_data.get("distance_to_work", 0)
    car_type = transportation_data.get("type", "")

    # Transportation Recommendations
    if mode_of_transport == "car":
        car_emissions = user_footprints.get("transportation", 0)

        if distance_to_work <= 5:
            savings = car_emissions * 0.15  # Assume 15% reduction for short-distance cycling
            recommendations.append(("Consider cycling or walking for short commutes.", savings))
        else:
            savings = car_emissions * 0.70  # Assume 70% reduction for using public transport for long distances
            recommendations.append(("Consider using tube or public buses.", savings))

        if car_type in ["petrol", "diesel"]:
            savings = car_emissions * 0.2  # Assume 20% savings for carpooling
            recommendations.append(("Switch to carpooling or public transport to reduce emissions.", savings))

    # Diet Recommendations
    if diet_data.get("beef_per_kg", 0) > 1.5:
        beef_savings = diet_data["beef_per_kg"] * 40.0 / 2  
        recommendations.append(("Reduce your beef consumption by 50% per week.", beef_savings))

    if diet_data.get("chicken_per_kg", 0) > 1:
        chicken_savings = diet_data["chicken_per_kg"] * 8.0 / 2
        recommendations.append(("Reduce your chicken consumption by 50% per week.", chicken_savings))

    if diet_data.get("fish_per_kg", 0) > 1:
        fish_savings = diet_data["fish_per_kg"] * 4.0 / 2
        recommendations.append(("Reduce your fish consumption by 50% per week.", fish_savings))

    if diet_data.get("milk_liters_per_week", 0) > 2:
        milk_savings = diet_data["milk_liters_per_week"] * 1.25 / 2
        recommendations.append(("Reduce your milk consumption by 50% per week.", milk_savings))

    if diet_data.get("eggs_per_week", 0) > 3:
        egg_savings = 2 * (2.2 / 12)
        recommendations.append(("Reduce your egg consumption by 2 per week.", egg_savings))

    if diet_data.get("vegan_meals_per_week", 0) == 0:
        vegan_savings = 8  # Assume fixed savings for introducing vegan meals
        recommendations.append(("Try incorporating at least 1 plant-based meal per week.", vegan_savings))

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
