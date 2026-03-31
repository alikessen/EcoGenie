import pytest

from modules.diet_module import calculate_diet_footprint
from modules.form_parsers import parse_transport_form
from modules.energy_module import calculate_energy_footprint
from modules.recommendation_module import generate_logical_recommendations
from modules.transportation_module import calculate_transport_footprint


def test_calculate_diet_footprint_basic():
    result = calculate_diet_footprint(
        {
            "beef_per_kg": 1,
            "chicken_per_kg": 0,
            "fish_per_kg": 0,
            "milk_liters_per_week": 0,
            "eggs_per_week": 0,
            "vegan_meals_per_week": 0,
        }
    )
    assert result > 90


def test_calculate_energy_footprint_uses_canonical_source():
    result = calculate_energy_footprint(
        {
            "electricity_kwh_per_month": 100,
            "electricity_source": "mixed",
            "heating_type": "none",
            "gas_usage_cubic_meters": 0,
            "energy_efficient_appliances": "no",
        }
    )
    assert result > 0


def test_calculate_energy_footprint_rejects_invalid_source():
    with pytest.raises(ValueError):
        calculate_energy_footprint(
            {
                "electricity_kwh_per_month": 100,
                "electricity_source": "some",
                "heating_type": "none",
                "gas_usage_cubic_meters": 0,
                "energy_efficient_appliances": "no",
            }
        )


def test_calculate_transport_footprint_public_transport_key():
    result = calculate_transport_footprint(
        {
            "work_distance_km": 10,
            "work_days": 5,
            "work_mode": "public transport",
            "work_car_type": "",
            "work_pt_type": "bus",
            "leisure_distance": 0,
            "leisure_days": 0,
            "leisure_mode": "",
            "leisure_type": "",
        }
    )
    assert result > 0


def test_recommendations_use_canonical_energy_values():
    recs = generate_logical_recommendations(
        transportation_data={
            "work_mode": "public transport",
            "work_distance_km": 10,
            "work_days": 5,
            "work_car_type": "",
            "work_pt_type": "bus",
            "leisure_mode": "",
            "leisure_distance": 0,
            "leisure_days": 0,
            "leisure_type": "",
        },
        diet_data={
            "beef_per_kg": 0,
            "chicken_per_kg": 0,
            "fish_per_kg": 0,
            "milk_liters_per_week": 0,
            "eggs_per_week": 0,
            "vegan_meals_per_week": 10,
        },
        energy_data={
            "electricity_source": "non_renewable",
            "gas_usage_cubic_meters": 0,
            "energy_efficient_appliances": "yes",
        },
        user_footprints={"energy": 50, "transportation": 10, "diet": 0},
    )

    assert any("renewable energy provider" in text.lower() for text, _ in recs)


def test_parse_transport_form_rejects_work_days_above_seven():
    with pytest.raises(ValueError, match="work_days must be between 0 and 7"):
        parse_transport_form(
            {
                "working": "yes",
                "work_mode": "car",
                "work_car_type": "petrol",
                "work_distance_km": "5",
                "work_days": "8",
                "leisure_distance": "0",
                "leisure_days": "0",
                "leisure_mode": "",
                "leisure_type": "",
            }
        )


def test_parse_transport_form_rejects_negative_leisure_days():
    with pytest.raises(ValueError, match="leisure_days must be between 0 and 7"):
        parse_transport_form(
            {
                "working": "no",
                "work_mode": "",
                "work_car_type": "",
                "work_distance_km": "0",
                "work_days": "0",
                "leisure_distance": "5",
                "leisure_days": "-1",
                "leisure_mode": "walk",
                "leisure_type": "",
            }
        )
