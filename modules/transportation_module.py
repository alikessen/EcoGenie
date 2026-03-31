from modules.carbon_data import carbon_data


def calculate_transport_footprint(transport_data):
    try:
        footprint = 0.0

        work_distance_km = transport_data.get("work_distance_km", 0)
        work_days = transport_data.get("work_days", 0)
        work_mode = transport_data.get("work_mode", "")
        work_car_type = transport_data.get("work_car_type", "")
        work_pt_type = transport_data.get("work_pt_type", "")
        total_work_distance = work_distance_km * work_days

        if work_mode == "car":
            footprint += total_work_distance * carbon_data["transport"][f"car_{work_car_type}"]
        elif work_mode == "public transport":
            footprint += total_work_distance * carbon_data["transport"][work_pt_type]

        leisure_distance = transport_data.get("leisure_distance", 0)
        leisure_days = transport_data.get("leisure_days", 0)
        leisure_mode = transport_data.get("leisure_mode", "")
        leisure_type = transport_data.get("leisure_type", "")
        total_leisure_distance = leisure_distance * leisure_days

        if leisure_mode == "car":
            footprint += total_leisure_distance * carbon_data["transport"][f"car_{leisure_type}"]
        elif leisure_mode == "public transport":
            footprint += total_leisure_distance * carbon_data["transport"][leisure_type]

        return footprint
    except KeyError as exc:
        raise ValueError(f"Missing CO2 data for: {exc}")


# Backward-compatible alias.
def calculateTransportFootprint(transport_data):
    return calculate_transport_footprint(transport_data)


def get_transport_data():
    return {
        "work_distance_km": 10,
        "work_days": 5,
        "work_mode": "car",
        "work_car_type": "petrol",
        "leisure_distance": 8,
        "leisure_days": 2,
        "leisure_mode": "public transport",
        "leisure_type": "bus",
    }


if __name__ == "__main__":
    sample_data = get_transport_data()
    print("Transport Carbon Footprint:", calculate_transport_footprint(sample_data))
