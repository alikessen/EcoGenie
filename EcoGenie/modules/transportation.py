def getTransportationData():
    print("Transportation Details:\n")

    while True:
        # Ask if the user is working
        working = input("Are you working? (yes/no): ").strip().lower()
        if working in ["yes", "no"]:
            break
        print("Invalid input. Please type 'yes' or 'no'.")

    total_travel_days = 0
    total_distance = 0
    transport_mode = None
    travel_type = None

    # Collect Work Travel Data
    if working == "yes":
        while True:
            try:
                distance_to_work = float(input("Enter the one-way distance between your home and work (in kilometers): ").strip())
                if distance_to_work >= 0:
                    break
                print("Distance cannot be negative. Please enter a valid distance.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            try:
                work_days = int(input("How many days do you commute to work in a typical week? (1-7): ").strip())
                if 1 <= work_days <= 7:
                    break
                print("Invalid input. Please enter a numeric value between 1 and 7.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            transport_mode = input("How do you go to work? (walk/cycle/public transport/car): ").strip().lower()
            if transport_mode in ["walk", "cycle", "public transport", "car"]:
                if transport_mode == "public transport":
                    while True:
                        travel_type = input("Do you use a bus, tube, or both? (bus/tube/both): ").strip().lower()
                        if travel_type in ["bus", "tube", "both"]:
                            break
                        print("Invalid input. Please type 'bus', 'tube', or 'both'.")
                elif transport_mode == "car":
                    while True:
                        travel_type = input("What type of car do you drive? (petrol/diesel/electric): ").strip().lower()
                        if travel_type in ["petrol", "diesel", "electric"]:
                            break
                        print("Invalid input. Please type 'petrol', 'diesel', or 'electric'.")
                break
            print("Invalid input. Please type 'walk', 'cycle', 'public transport', or 'car'.")

        total_travel_days += work_days
        total_distance += distance_to_work * 2 * work_days  # Round-trip travel

    # Collect Leisure (Non-Work) Travel Data
    while True:
        try:
            leisure_days = int(input("How many additional days per week do you travel for errands, shopping, or social activities? (0-7): ").strip())
            if 0 <= leisure_days <= 7:
                break
            print("Invalid input. Please enter a number between 0 and 7.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    if leisure_days > 0:
        while True:
            try:
                leisure_distance = float(input("On average, how many kilometers do you travel per day for these activities? ").strip())
                if leisure_distance >= 0:
                    break
                print("Distance cannot be negative. Please enter a valid distance.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            leisure_mode = input("How do you usually travel for these activities? (walk/cycle/public transport/car): ").strip().lower()
            if leisure_mode in ["walk", "cycle", "public transport", "car"]:
                if leisure_mode == "public transport":
                    while True:
                        leisure_type = input("Do you use a bus, tube, or both? (bus/tube/both): ").strip().lower()
                        if leisure_type in ["bus", "tube", "both"]:
                            break
                        print("Invalid input. Please type 'bus', 'tube', or 'both'.")
                elif leisure_mode == "car":
                    while True:
                        leisure_type = input("What type of car do you drive? (petrol/diesel/electric): ").strip().lower()
                        if leisure_type in ["petrol", "diesel", "electric"]:
                            break
                        print("Invalid input. Please type 'petrol', 'diesel', or 'electric'.")
                break
            print("Invalid input. Please type 'walk', 'cycle', 'public transport', or 'car'.")

        total_travel_days += leisure_days
        total_distance += leisure_distance * leisure_days  # Total weekly distance

    return {
        "working": working,
        "total_travel_days": total_travel_days,
        "total_distance": total_distance,
        "work_mode": transport_mode,
        "work_type": travel_type,
        "leisure_mode": leisure_mode if leisure_days > 0 else None,
        "leisure_type": leisure_type if leisure_days > 0 else None,
    }


def calculateTransportFootprint(transportation_data):
    carbon_data = {
        "car_types": {
            "petrol": 0.165,  
            "diesel": 0.17,
            "electric": 0.0,  
        },
        "public_transport": {
            "bus": 0.075,  
            "tube": 0.025,
        },
    }

    footprint = 0.0
    total_distance = transportation_data.get("total_distance", 0)  

    # Calculate emissions from work travel
    if transportation_data.get("work_mode") == "car":
        footprint += total_distance * carbon_data["car_types"].get(transportation_data.get("work_type", ""), 0)
    elif transportation_data.get("work_mode") == "public transport":
        if transportation_data.get("work_type") == "bus":
            footprint += total_distance * carbon_data["public_transport"]["bus"]
        elif transportation_data.get("work_type") == "tube":
            footprint += total_distance * carbon_data["public_transport"]["tube"]
        elif transportation_data.get("work_type") == "both":
            footprint += total_distance * ((carbon_data["public_transport"]["bus"] + carbon_data["public_transport"]["tube"]) / 2)

    # Calculate emissions from leisure travel
    leisure_mode = transportation_data.get("leisure_mode", "") 
    leisure_type = transportation_data.get("leisure_type", "")

    if leisure_mode == "car":
        footprint += total_distance * carbon_data["car_types"].get(leisure_type, 0)
    elif leisure_mode == "public transport":
        if leisure_type == "bus":
            footprint += total_distance * carbon_data["public_transport"]["bus"]
        elif leisure_type == "tube":
            footprint += total_distance * carbon_data["public_transport"]["tube"]
        elif leisure_type == "both":
            footprint += total_distance * ((carbon_data["public_transport"]["bus"] + carbon_data["public_transport"]["tube"]) / 2)

    return footprint


