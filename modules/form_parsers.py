from typing import Mapping

ELECTRICITY_SOURCE_MAP = {
    "yes": "renewable",
    "no": "non_renewable",
    "some": "mixed",
}

HEATING_TYPES = {"gas", "electric", "oil", "none"}
APPLIANCE_VALUES = {"yes", "no", "some"}
WORKING_VALUES = {"yes", "no"}
WORK_MODES = {"walk", "cycle", "public transport", "car"}
CAR_TYPES = {"petrol", "diesel", "electric"}
PUBLIC_TRANSPORT_TYPES = {"bus", "tube", "both"}
LEISURE_MODES = {"walk", "cycle", "public transport", "car", ""}
DIET_TYPES = {"vegan", "vegetarian", "neither"}


def _parse_float(value, field_name):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid numeric value for {field_name}")


def _validate_range(value, field_name, minimum, maximum):
    if value < minimum or value > maximum:
        raise ValueError(
            f"{field_name} must be between {minimum} and {maximum}"
        )
    return value


def _parse_int(value, field_name):
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid integer value for {field_name}")


def parse_diet_form(form: Mapping[str, str]):
    diet_type = form.get("diet_type", "")
    if diet_type not in DIET_TYPES:
        raise ValueError("Invalid diet type")

    return {
        "diet_type": diet_type,
        "beef_per_kg": _parse_float(form.get("beef_per_kg"), "beef_per_kg"),
        "chicken_per_kg": _parse_float(form.get("chicken_per_kg"), "chicken_per_kg"),
        "fish_per_kg": _parse_float(form.get("fish_per_kg"), "fish_per_kg"),
        "milk_liters_per_week": _parse_float(form.get("milk_liters_per_week"), "milk_liters_per_week"),
        "eggs_per_week": _parse_int(form.get("eggs_per_week"), "eggs_per_week"),
        "vegan_meals_per_week": _parse_int(form.get("vegan_meals_per_week"), "vegan_meals_per_week"),
    }


def parse_energy_form(form: Mapping[str, str]):
    electricity_kwh_per_month = _parse_float(
        form.get("electricity_kwh_per_month"),
        "electricity_kwh_per_month",
    )

    electricity_source_form_value = form.get("electricity_source", "")
    if electricity_source_form_value:
        if electricity_source_form_value not in ELECTRICITY_SOURCE_MAP:
            raise ValueError("Invalid electricity source")
        electricity_source = ELECTRICITY_SOURCE_MAP[electricity_source_form_value]
    else:
        electricity_source = ""

    heating_type = form.get("heating_type", "")
    if heating_type and heating_type not in HEATING_TYPES:
        raise ValueError("Invalid heating type")

    energy_efficient_appliances = form.get("energy_efficient_appliances", "")
    if energy_efficient_appliances and energy_efficient_appliances not in APPLIANCE_VALUES:
        raise ValueError("Invalid energy-efficient appliances value")

    gas_usage_cubic_meters = _parse_float(
        form.get("gas_usage_cubic_meters"),
        "gas_usage_cubic_meters",
    )

    return {
        "electricity_kwh_per_month": electricity_kwh_per_month,
        "electricity_source": electricity_source,
        "heating_type": heating_type,
        "gas_usage_cubic_meters": gas_usage_cubic_meters,
        "energy_efficient_appliances": energy_efficient_appliances,
    }


def parse_transport_form(form: Mapping[str, str]):
    working = form.get("working", "")
    if working not in WORKING_VALUES:
        raise ValueError("Invalid working value")

    work_distance_km = 0.0
    work_days = 0
    work_mode = ""
    work_car_type = ""
    work_pt_type = ""

    if working == "yes":
        work_mode = form.get("work_mode", "")
        if work_mode not in WORK_MODES:
            raise ValueError("Invalid work mode")

        if work_mode == "car":
            work_car_type = form.get("work_car_type", "")
            if work_car_type not in CAR_TYPES:
                raise ValueError("Invalid work car type")
        elif work_mode == "public transport":
            work_pt_type = form.get("work_pt_type", "")
            if work_pt_type not in PUBLIC_TRANSPORT_TYPES:
                raise ValueError("Invalid work public transport type")

        work_distance_km = _parse_float(form.get("work_distance_km"), "work_distance_km")
        work_days = _parse_int(form.get("work_days"), "work_days")
        work_days = _validate_range(work_days, "work_days", 0, 7)

    leisure_distance = _parse_float(form.get("leisure_distance"), "leisure_distance")
    leisure_days = _parse_int(form.get("leisure_days"), "leisure_days")
    leisure_days = _validate_range(leisure_days, "leisure_days", 0, 7)
    leisure_mode = form.get("leisure_mode", "")
    if leisure_mode not in LEISURE_MODES:
        raise ValueError("Invalid leisure mode")

    leisure_type = form.get("leisure_type", "")
    if leisure_mode == "car" and leisure_type not in CAR_TYPES:
        raise ValueError("Invalid leisure car type")
    if leisure_mode == "public transport" and leisure_type not in PUBLIC_TRANSPORT_TYPES:
        raise ValueError("Invalid leisure public transport type")

    return {
        "working": working,
        "work_distance_km": work_distance_km,
        "work_days": work_days,
        "work_mode": work_mode,
        "work_car_type": work_car_type,
        "work_pt_type": work_pt_type,
        "leisure_distance": leisure_distance,
        "leisure_days": leisure_days,
        "leisure_mode": leisure_mode,
        "leisure_type": leisure_type,
    }
