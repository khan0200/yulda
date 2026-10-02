import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def test_create_and_get_listing(client):
    token = await signup_and_login(client, "cardealer@example.com", "CarDealer")
    response = await client.post(
        "/api/v1/auto/listings",
        json={
            "listing_type": "SALE",
            "make": "Hyundai",
            "model": "Sonata",
            "year": 2021,
            "mileage_km": 35000,
            "fuel_type": "GASOLINE",
            "transmission": "AUTOMATIC",
            "price": 18000000,
            "description": "Single owner, well maintained",
            "contact_value": "010-3333-4444",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["make"] == "Hyundai"
    assert body["year"] == 2021
    assert body["owner"]["name"] == "CarDealer"

    listing_id = body["id"]
    get_response = await client.get(f"/api/v1/auto/listings/{listing_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["mileage_km"] == 35000


async def test_rental_listing_with_daily_price(client):
    token = await signup_and_login(client, "rentalco@example.com", "RentalCo")
    response = await client.post(
        "/api/v1/auto/listings",
        json={
            "listing_type": "RENTAL",
            "make": "Kia",
            "model": "Morning",
            "year": 2022,
            "mileage_km": 10000,
            "fuel_type": "GASOLINE",
            "transmission": "AUTOMATIC",
            "price": 0,
            "rental_price_per_day": 45000,
            "description": "Daily rental, insurance included",
            "contact_value": "010-7777-6666",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    assert response.json()["data"]["rental_price_per_day"] == 45000
    assert response.json()["data"]["listing_type"] == "RENTAL"


async def test_create_listing_requires_auth(client):
    response = await client.post(
        "/api/v1/auto/listings",
        json={
            "listing_type": "SALE",
            "make": "Chevrolet",
            "model": "Spark",
            "year": 2019,
            "mileage_km": 80000,
            "fuel_type": "GASOLINE",
            "transmission": "MANUAL",
            "price": 6000000,
            "description": "desc",
            "contact_value": "010-0000-0000",
        },
    )
    assert response.status_code == 401


async def test_list_listings_filters_by_make_and_fuel_type(client):
    token = await signup_and_login(client, "fleetowner@example.com", "FleetOwner")
    cars = [
        ("Hyundai", "GASOLINE"),
        ("Hyundai", "ELECTRIC"),
        ("Kia", "ELECTRIC"),
    ]
    for make, fuel in cars:
        await client.post(
            "/api/v1/auto/listings",
            json={
                "listing_type": "SALE",
                "make": make,
                "model": "Test",
                "year": 2023,
                "mileage_km": 5000,
                "fuel_type": fuel,
                "transmission": "AUTOMATIC",
                "price": 20000000,
                "description": "desc",
                "contact_value": "010-1111-1111",
            },
            headers=auth_headers(token),
        )

    response = await client.get("/api/v1/auto/listings", params={"make": "Hyundai", "fuel_type": "ELECTRIC"})
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["make"] == "Hyundai"
    assert data["items"][0]["fuel_type"] == "ELECTRIC"


async def test_year_range_filter(client):
    token = await signup_and_login(client, "vintage@example.com", "Vintage")
    for year in [2015, 2020, 2024]:
        await client.post(
            "/api/v1/auto/listings",
            json={
                "listing_type": "SALE",
                "make": "Genesis",
                "model": "G80",
                "year": year,
                "mileage_km": 1000,
                "fuel_type": "DIESEL",
                "transmission": "AUTOMATIC",
                "price": 30000000,
                "description": "desc",
                "contact_value": "010-2222-2222",
            },
            headers=auth_headers(token),
        )

    response = await client.get("/api/v1/auto/listings", params={"min_year": 2018, "max_year": 2022})
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["year"] == 2020


async def test_only_owner_can_delete_listing(client):
    owner_token = await signup_and_login(client, "autoowner@example.com", "AutoOwner")
    other_token = await signup_and_login(client, "autostranger@example.com", "AutoStranger")

    create = await client.post(
        "/api/v1/auto/listings",
        json={
            "listing_type": "SALE",
            "make": "Toyota",
            "model": "Camry",
            "year": 2020,
            "mileage_km": 40000,
            "fuel_type": "HYBRID",
            "transmission": "AUTOMATIC",
            "price": 22000000,
            "description": "desc",
            "contact_value": "010-4444-3333",
        },
        headers=auth_headers(owner_token),
    )
    listing_id = create.json()["data"]["id"]

    forbidden = await client.delete(f"/api/v1/auto/listings/{listing_id}", headers=auth_headers(other_token))
    assert forbidden.status_code == 403

    allowed = await client.delete(f"/api/v1/auto/listings/{listing_id}", headers=auth_headers(owner_token))
    assert allowed.status_code == 200
