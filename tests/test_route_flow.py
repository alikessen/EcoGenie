from modules.form_parsers import ELECTRICITY_SOURCE_MAP


def test_happy_path_route_flow(logged_in_client):
    client = logged_in_client

    diet_resp = client.post(
        "/diet",
        data={
            "diet_type": "neither",
            "beef_per_kg": "1",
            "chicken_per_kg": "1",
            "fish_per_kg": "0",
            "milk_liters_per_week": "1",
            "eggs_per_week": "4",
            "vegan_meals_per_week": "2",
        },
        follow_redirects=False,
    )
    assert diet_resp.status_code == 302
    assert "/energy" in diet_resp.location

    energy_resp = client.post(
        "/energy",
        data={
            "electricity_kwh_per_month": "250",
            "electricity_source": "some",
            "heating_type": "gas",
            "gas_usage_cubic_meters": "40",
            "energy_efficient_appliances": "yes",
        },
        follow_redirects=False,
    )
    assert energy_resp.status_code == 302
    assert "/transportation" in energy_resp.location

    transport_resp = client.post(
        "/transportation",
        data={
            "working": "yes",
            "work_distance_km": "10",
            "work_days": "5",
            "work_mode": "public transport",
            "work_pt_type": "bus",
            "leisure_days": "1",
            "leisure_distance": "5",
            "leisure_mode": "walk",
            "leisure_type": "",
        },
        follow_redirects=False,
    )
    assert transport_resp.status_code == 302
    assert "/recommendations" in transport_resp.location

    page = client.get("/recommendations")
    assert page.status_code == 200

    with client.session_transaction() as sess:
        assert sess["energy"]["electricity_source"] == ELECTRICITY_SOURCE_MAP["some"]
        assert sess["transportation"]["work_pt_type"] == "bus"


def test_transportation_rejects_days_out_of_range(logged_in_client):
    client = logged_in_client
    response = client.post(
        "/transportation",
        data={
            "working": "yes",
            "work_distance_km": "10",
            "work_days": "8",
            "work_mode": "public transport",
            "work_pt_type": "bus",
            "leisure_days": "1",
            "leisure_distance": "5",
            "leisure_mode": "walk",
            "leisure_type": "",
        },
        follow_redirects=False,
    )
    assert response.status_code == 400
    assert b"work_days must be between 0 and 7" in response.data
