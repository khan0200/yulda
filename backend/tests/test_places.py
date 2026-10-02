import pytest

pytestmark = pytest.mark.asyncio


async def _insert_seed_place(db, name: str, country: str, population: int = 1000):
    await db.places.insert_one(
        {
            "name": name,
            "ascii_name": name,
            "alt_names": [],
            "country": country,
            "admin1": None,
            "population": population,
            "lat": 0.0,
            "lon": 0.0,
            "source": "SEED",
            "usage_count": 0,
        }
    )


async def test_search_returns_prefix_matches(client, db):
    await _insert_seed_place(db, "Seoul", "KR", population=10000000)
    await _insert_seed_place(db, "Seongnam", "KR", population=900000)
    await _insert_seed_place(db, "Busan", "KR", population=3000000)

    response = await client.get("/api/v1/places/search", params={"q": "Se"})
    assert response.status_code == 200
    names = [p["name"] for p in response.json()["data"]]
    assert "Seoul" in names
    assert "Seongnam" in names
    assert "Busan" not in names


async def test_search_is_case_insensitive(client, db):
    await _insert_seed_place(db, "Tashkent", "UZ")
    response = await client.get("/api/v1/places/search", params={"q": "tash"})
    assert response.status_code == 200
    assert response.json()["data"][0]["name"] == "Tashkent"


async def test_search_filters_by_country(client, db):
    await _insert_seed_place(db, "Samarkand", "UZ")
    await _insert_seed_place(db, "Samara", "RU")

    response = await client.get("/api/v1/places/search", params={"q": "Sam", "country": "UZ"})
    assert response.status_code == 200
    names = [p["name"] for p in response.json()["data"]]
    assert names == ["Samarkand"]


async def test_search_whitespace_query_returns_empty_list(client):
    response = await client.get("/api/v1/places/search", params={"q": " "})
    assert response.status_code == 200
    assert response.json()["data"] == []


async def test_learn_new_place_creates_user_sourced_entry(client):
    response = await client.post("/api/v1/places", json={"name": "Yangi Qishloq", "country": "UZ"})
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["name"] == "Yangi Qishloq"
    assert body["source"] == "USER"
    assert body["usage_count"] == 1

    search_response = await client.get("/api/v1/places/search", params={"q": "Yangi", "country": "UZ"})
    names = [p["name"] for p in search_response.json()["data"]]
    assert "Yangi Qishloq" in names


async def test_learn_existing_place_increments_usage_count(client):
    first = await client.post("/api/v1/places", json={"name": "New Town", "country": "KR"})
    second = await client.post("/api/v1/places", json={"name": "New Town", "country": "KR"})
    assert first.json()["data"]["usage_count"] == 1
    assert second.json()["data"]["usage_count"] == 2
    assert first.json()["data"]["id"] == second.json()["data"]["id"]


async def test_search_ranks_by_usage_then_population(client, db):
    await _insert_seed_place(db, "Townville Low", "KR", population=100)
    await _insert_seed_place(db, "Townville High", "KR", population=500000)
    for _ in range(5):
        await client.post("/api/v1/places", json={"name": "Townville Used", "country": "KR"})

    response = await client.get("/api/v1/places/search", params={"q": "Town", "country": "KR"})
    names = [p["name"] for p in response.json()["data"]]
    assert names[0] == "Townville Used"
    assert names.index("Townville High") < names.index("Townville Low")
