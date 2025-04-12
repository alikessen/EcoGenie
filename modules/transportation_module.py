from modules.carbon_data import carbon_data

def calculateTransportFootprint(transport_data):
    """Calculates the transport-related carbon footprint using values from CSV."""
    try:
        footprint = 0.0

        # Work-related emissions
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
        elif work_mode in ["walk", "cycle"]:
            footprint += 0.0  # Zero-emission transport

        # Leisure-related emissions
        leisure_distance = transport_data.get("leisure_distance", 0)
        leisure_days = transport_data.get("leisure_days", 0)
        leisure_mode = transport_data.get("leisure_mode", "")
        leisure_type = transport_data.get("leisure_type", "")
        total_leisure_distance = leisure_distance * leisure_days

        if leisure_mode == "car":
            footprint += total_leisure_distance * carbon_data["transport"][f"car_{leisure_type}"]
        elif leisure_mode == "public transport":
            footprint += total_leisure_distance * carbon_data["transport"][leisure_type]
        elif leisure_mode in ["walk", "cycle"]:
            footprint += 0.0  # Zero-emission leisure transport

        return footprint

    except KeyError as e:
        raise ValueError(f"Missing CO₂ data for: {e}")


def getTransportData():
    """CLI-based collection of transportation input (for testing only)."""
    try:
        print("Transportation Details:\n")

        data = {
            "work_distance_km": 10,
            "work_days": 5,
            "work_mode": "car",
            "work_type": "petrol",
            "leisure_distance": 8,
            "leisure_days": 2,
            "leisure_mode": "public transport",
            "leisure_type": "bus"
        }

        return data

    except Exception as e:
        raise ValueError(f"Input error: {e}")


if __name__ == "__main__":
    sample_data = getTransportData()
    print("Transport Carbon Footprint:", calculateTransportFootprint(sample_data))
