from modules.carbon_data import carbon_data

def getTransportData():
    """Collects user input for transportation habits and returns a structured dictionary."""
    print("Transportation Details:\n")

    while True:
        working = input("Do you commute to work/school? (yes/no): ").strip().lower()
        if working in ["yes", "no"]:
            break
        print("Invalid input. Please type 'yes' or 'no'.")

    work_distance_km = 0
    work_days = 0
    work_mode = None
    work_type = None

    if working == "yes":
        while True:
            try:
                work_distance_km = float(input("How many kilometers is your one-way commute? (0-100): ").strip())
                if 0 <= work_distance_km <= 100:
                    break
                print("Invalid input. Please enter a number between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            try:
                work_days = int(input("How many days per week do you commute? (1-7): ").strip())
                if 1 <= work_days <= 7:
                    break
                print("Invalid input. Please enter a number between 1 and 7.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        while True:
            work_mode = input("How do you commute? (walk/cycle/public transport/car): ").strip().lower()
            if work_mode in ["walk", "cycle", "public transport", "car"]:
                break
            print("Invalid input. Please type 'walk', 'cycle', 'public transport', or 'car'.")

        if work_mode == "car":
            while True:
                work_type = input("What type of car do you drive? (petrol/diesel/electric): ").strip().lower()
                if work_type in ["petrol", "diesel", "electric"]:
                    break
                print("Invalid input. Please type 'petrol', 'diesel', or 'electric'.")

        if work_mode == "public transport":
            while True:
                work_type = input("What public transport do you use? (bus/tube/both): ").strip().lower()
                if work_type in ["bus", "tube", "both"]:
                    break
                print("Invalid input. Please type 'bus', 'tube', or 'both'.")


    return {
        "work_distance_km": work_distance_km,
        "work_days": work_days,
        "work_mode": work_mode,
        "work_type": work_type,
    }

def calculateTransportFootprint(transport_data):
    """Calculates the transport-related carbon footprint using values from CSV."""
    footprint = 0.0
    total_distance = transport_data["work_distance_km"] * transport_data["work_days"]  # Remove *2

    if transport_data["work_mode"] == "car":
        car_type = transport_data["work_type"]
        footprint += total_distance * carbon_data["transport"].get(f"car_{car_type}", 0.15)  # Default 0.15 kg CO2/km

    elif transport_data["work_mode"] == "public transport":
        transport_type = transport_data["work_type"]
        if transport_type in ["bus", "tube", "both"]:
            footprint += total_distance * carbon_data["transport"].get(transport_type, 0.05)  # Default 0.05 kg CO2/km

    return footprint


if __name__ == "__main__":
    sample_data = {
        "work_distance_km": 10,
        "work_days": 5,
        "work_mode": "car",
        "work_type": "petrol"
    }
    print("Transport Carbon Footprint:", calculateTransportFootprint(sample_data))