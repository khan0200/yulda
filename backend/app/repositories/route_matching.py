from datetime import datetime, timedelta
from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection


def normalize_stop_name(name: str) -> str:
    return name.strip().lower()


def route_matches(stop_names_lower: list[str], from_city: str | None, to_city: str | None) -> bool:
    """True if from_city appears before to_city in the ordered stop list.

    Done in Python (not a Mongo $expr/$indexOfArray pipeline) because that
    aggregation operator isn't supported by mongomock, which the test suite
    relies on, and candidate sets here are small enough that this is cheap.
    """
    if from_city and to_city:
        if from_city not in stop_names_lower or to_city not in stop_names_lower:
            return False
        return stop_names_lower.index(from_city) < stop_names_lower.index(to_city)
    if from_city:
        return from_city in stop_names_lower
    if to_city:
        return to_city in stop_names_lower
    return True


def day_bounds(day: datetime) -> tuple[datetime, datetime]:
    start = day.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


def base_query(post_type: str | None, date: datetime | None) -> dict[str, Any]:
    query: dict[str, Any] = {"status": "ACTIVE"}
    if post_type:
        query["post_type"] = post_type
    if date:
        start, end = day_bounds(date)
        query["departure_at"] = {"$gte": start, "$lt": end}
    return query


async def search_routes(
    collection: AsyncIOMotorCollection,
    post_type: str | None,
    from_city: str | None,
    to_city: str | None,
    date: datetime | None,
    page: int,
    page_size: int,
) -> tuple[list[dict[str, Any]], int]:
    query = base_query(post_type, date)
    from_norm = normalize_stop_name(from_city) if from_city else None
    to_norm = normalize_stop_name(to_city) if to_city else None

    if from_norm:
        query["stop_names_lower"] = from_norm if not to_norm else {"$all": [from_norm, to_norm]}
    elif to_norm:
        query["stop_names_lower"] = to_norm

    cursor = collection.find(query).sort("departure_at", 1)
    all_matches = await cursor.to_list(length=None)
    filtered = [doc for doc in all_matches if route_matches(doc["stop_names_lower"], from_norm, to_norm)]

    total = len(filtered)
    start_idx = (page - 1) * page_size
    page_items = filtered[start_idx : start_idx + page_size]
    return page_items, total


async def search_nearby_dates(
    collection: AsyncIOMotorCollection,
    post_type: str | None,
    from_city: str,
    to_city: str,
    center_date: datetime,
    window_days: int,
    limit: int,
) -> list[dict[str, Any]]:
    from_norm = normalize_stop_name(from_city)
    to_norm = normalize_stop_name(to_city)

    query = base_query(post_type, date=None)
    query["stop_names_lower"] = {"$all": [from_norm, to_norm]}
    start = center_date - timedelta(days=window_days)
    end = center_date + timedelta(days=window_days + 1)
    query["departure_at"] = {"$gte": start, "$lt": end}

    cursor = collection.find(query).sort("departure_at", 1)
    all_matches = await cursor.to_list(length=None)
    filtered = [doc for doc in all_matches if route_matches(doc["stop_names_lower"], from_norm, to_norm)]
    return filtered[:limit]
