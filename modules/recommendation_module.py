from modules.carbon_data import carbon_data


def generateLogicalRecommendations(transportation_data, diet_data, energy_data, user_footprints):
    recommendations = []

    # Transport: Work travel
    mode_of_transport = transportation_data.get("work_mode", "")
    distance_to_work = transportation_data.get("work_distance_km", 0)
    work_days = transportation_data.get("work_days", 0)
    work_car_type = transportation_data.get("work_car_type", "")
    work_pt_type = transportation_data.get("work_public_transport_type", "")
    transport_footprint = user_footprints.get("transportation", 0)
    total_distance_work = work_days * distance_to_work * 2

    if mode_of_transport == "car":
        emission_factor = carbon_data["transport"][f"car_{work_car_type}"]

        if distance_to_work <= 5:
            savings = total_distance_work * emission_factor
            recommendations.append(("Consider walking or cycling to work.", savings))

        elif distance_to_work > 5 and work_car_type != "electric":
            savings = (total_distance_work * emission_factor) - (total_distance_work * carbon_data["transport"]["both"])
            recommendations.append(("Switch to public transport for long commutes to reduce emissions.", savings))

    elif mode_of_transport == "public transport" and work_pt_type == "bus":
        savings = (total_distance_work * carbon_data["transport"]["bus"]) - (total_distance_work * carbon_data["transport"]["tube"])
        recommendations.append(("Switch from bus to tube if possible for faster and cleaner commutes.", savings))

    # Transport: Leisure travel
    leisure_mode = transportation_data.get("leisure_mode", "")
    leisure_distance = transportation_data.get("leisure_distance", 0)
    leisure_days = transportation_data.get("leisure_days", 0)
    leisure_type = transportation_data.get("leisure_type", "")
    total_distance_leisure = leisure_days * leisure_distance * 2

    if leisure_mode == "car":
        leisure_emission_factor = carbon_data["transport"].get(f"car_{leisure_type}", 0)

        if leisure_emission_factor > 0:
            savings = total_distance_leisure * leisure_emission_factor / 2
            recommendations.append(("Reduce leisure car travel by %50 per week", savings))

    elif leisure_mode == "public transport" and leisure_type == "bus":
        bus_emission_factor = carbon_data["transport"].get("bus", 0)
        tube_emission_factor = carbon_data["transport"].get("tube", 0)
        savings = total_distance_leisure * (bus_emission_factor - tube_emission_factor)
        recommendations.append(("Use the tube instead of the bus for lower emissions during leisure trips.", savings))

   
    # Diet Recommendations
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

    if 7 > diet_data.get("eggs_per_week", 0) > 3:
        egg_emission = carbon_data["diet"]["eggs"]
        egg_savings = 2 * egg_emission  
        recommendations.append(("Reduce your egg consumption by 2 per week.", egg_savings))
    
    elif diet_data.get("eggs_per_week", 0) > 7:
        egg_emission = carbon_data["diet"]["eggs"]
        egg_savings = 3 * egg_emission  
        recommendations.append(("Reduce your egg consumption by 3 per week.", egg_savings))


    vegan_meals = int(diet_data.get("vegan_meals_per_week", 0))

    if vegan_meals < 7:
        avg_meal_emission = carbon_data["diet"]["average_meal"]
        vegan_meal_emission = carbon_data["diet"]["vegan_meals"]
        co2_saved_per_meal = avg_meal_emission - vegan_meal_emission
        vegan_savings = co2_saved_per_meal * (7 - diet_data["vegan_meals_per_week"])

        recommendations.append(("Try making your breakfasts plant-based 7 times per week.", vegan_savings))

    elif 7 <= vegan_meals < 14:
        avg_meal_emission = carbon_data["diet"]["average_meal"]
        vegan_meal_emission = carbon_data["diet"]["vegan_meals"]
        co2_saved_per_meal = avg_meal_emission - vegan_meal_emission
        needed_meals = 15 - diet_data["vegan_meals_per_week"]
        vegan_savings = co2_saved_per_meal * needed_meals

        recommendations.append((f"Try increasing your plant-based meals by {needed_meals} more per week.", vegan_savings))



    # Energy Recommendations
    electricity_source = energy_data.get("electricity_source", "")
    electricity_footprint = user_footprints.get("energy", 0)

    # Suggest switching to renewable electricity
    if electricity_source == "no":
        recommendations.append((
            "Switch to a renewable energy provider to eliminate electricity emissions.", 
            electricity_footprint
        ))

    elif electricity_source == "some":
        savings = electricity_footprint * 0.5
        recommendations.append((
            "Switch to a fully renewable energy provider to cut electricity emissions by 50%.", 
            savings
        ))

    # Suggest reducing gas usage if high
    gas_usage = energy_data.get("gas_usage_cubic_meters", 0)
    gas_emission_factor = carbon_data["energy"]["gas"]
    gas_footprint = gas_usage * gas_emission_factor
    if gas_usage > 50:
        savings = gas_footprint * 0.1  
        recommendations.append((
            "Reduce gas heating usage by 10%.", 
            savings
        ))

    # Suggest upgrading appliances proportionally
    if energy_data.get("energy_efficient_appliances", "") == "no":
        appliance_savings = electricity_footprint * 0.15 * 0.3  # 15% of usage saved by 30%
        recommendations.append((
            "Upgrade to energy-efficient appliances or install LED bulbs.", 
            appliance_savings
        ))

    # Filter out empty or zero-saving recommendations
    recommendations = [(text, saving) for text, saving in recommendations if saving > 0]

    # Sort by highest saving
    recommendations.sort(key=lambda x: x[1], reverse=True)

    # Return the sorted list 
    return recommendations[:10]

