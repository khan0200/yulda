import json
import logging
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from app.core.config import settings

logger = logging.getLogger("yulda.database")

PLACES_SEED_PATH = Path(__file__).resolve().parent.parent / "data" / "places_seed.json"

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGODB_URI)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    global _db
    if _db is None:
        _db = get_client()[settings.MONGODB_DATABASE]
    return _db


async def connect_to_mongo() -> None:
    global _db

    if settings.ENV == "development":
        probe = AsyncIOMotorClient(settings.MONGODB_URI, serverSelectionTimeoutMS=1500)
        try:
            await probe.admin.command("ping")
            logger.info("Connected to MongoDB at %s", settings.MONGODB_URI)
        except PyMongoError:
            logger.warning(
                "No MongoDB reachable at %s — falling back to an in-memory mock database "
                "for local development. Data will NOT persist across restarts. "
                "Install/run real MongoDB (or docker compose up) for persistent data.",
                settings.MONGODB_URI,
            )
            from mongomock_motor import AsyncMongoMockClient

            _db = AsyncMongoMockClient()[settings.MONGODB_DATABASE]
        finally:
            probe.close()
    else:
        client = get_client()
        try:
            await client.admin.command("ping")
            logger.info("Connected to MongoDB at %s", settings.MONGODB_URI)
        except PyMongoError:
            logger.exception("Failed to connect to MongoDB")
            raise

    await ensure_indexes()
    await seed_places_if_empty()


async def seed_places_if_empty() -> None:
    db = get_database()
    try:
        existing = await db.places.estimated_document_count()
    except PyMongoError:
        logger.warning("Could not check places collection count — skipping seed")
        return

    if existing > 0:
        logger.info("Places collection already has %d documents — skipping seed", existing)
        return

    if not PLACES_SEED_PATH.exists():
        logger.warning("Places seed file not found at %s — skipping seed", PLACES_SEED_PATH)
        return

    with open(PLACES_SEED_PATH, encoding="utf-8") as f:
        raw_places = json.load(f)

    docs = [
        {
            "name": p["name"],
            "ascii_name": p["ascii_name"],
            "alt_names": p["alt_names"],
            "country": p["country"],
            "admin1": p["admin1"] or None,
            "population": p["population"],
            "lat": p["lat"],
            "lon": p["lon"],
            "source": "SEED",
            "usage_count": 0,
        }
        for p in raw_places
    ]

    try:
        await db.places.insert_many(docs, ordered=False)
        logger.info("Seeded %d places", len(docs))
    except PyMongoError:
        logger.exception("Failed to seed places")


async def close_mongo_connection() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


async def ensure_indexes() -> None:
    db = get_database()
    try:
        await _create_indexes(db)
        logger.info("MongoDB indexes ensured")
    except PyMongoError:
        if settings.ENV != "development":
            raise
        logger.warning("Some indexes could not be created against the mock database — skipping (dev mode only)")


async def _create_indexes(db: AsyncIOMotorDatabase) -> None:

    await db.users.create_index("email", unique=True, sparse=True)
    await db.users.create_index("phone", unique=True, sparse=True)
    await db.users.create_index("roles")

    await db.drivers.create_index("user_id", unique=True)
    await db.drivers.create_index([("current_location", "2dsphere")])
    await db.drivers.create_index("is_online")

    await db.rides.create_index("customer_id")
    await db.rides.create_index("driver_id")
    await db.rides.create_index("status")
    await db.rides.create_index("created_at")
    await db.rides.create_index([("pickup_location", "2dsphere")])

    await db.ride_events.create_index("ride_id")
    await db.ride_events.create_index("created_at")

    await db.deliveries.create_index("customer_id")
    await db.deliveries.create_index("courier_id")
    await db.deliveries.create_index("status")
    await db.deliveries.create_index([("pickup_location", "2dsphere")])

    await db.delivery_events.create_index("delivery_id")

    await db.jobs.create_index([("title", "text"), ("description", "text")])
    await db.jobs.create_index("employer_id")
    await db.jobs.create_index("category")
    await db.jobs.create_index("status")
    await db.jobs.create_index("created_at")
    await db.jobs.create_index([("location", "2dsphere")])

    await db.job_applications.create_index([("job_id", 1), ("applicant_id", 1)], unique=True)
    await db.job_applications.create_index("applicant_id")
    await db.job_applications.create_index("status")

    await db.services.create_index([("title", "text"), ("description", "text")])
    await db.services.create_index("category")
    await db.services.create_index("provider_id")
    await db.services.create_index([("location", "2dsphere")])

    await db.service_providers.create_index("user_id", unique=True)
    await db.service_providers.create_index([("location", "2dsphere")])

    await db.service_requests.create_index("customer_id")
    await db.service_requests.create_index("provider_id")
    await db.service_requests.create_index("status")

    await db.orders.create_index("user_id")
    await db.orders.create_index("type")
    await db.orders.create_index("status")
    await db.orders.create_index("created_at")

    await db.payments.create_index("order_id")
    await db.payments.create_index("user_id")
    await db.payments.create_index("status")
    await db.payments.create_index("provider_transaction_id")

    await db.transactions.create_index("user_id")
    await db.transactions.create_index("created_at")

    await db.wallets.create_index("user_id", unique=True)

    await db.withdrawals.create_index("user_id")
    await db.withdrawals.create_index("status")

    await db.conversations.create_index("participant_ids")
    await db.messages.create_index("conversation_id")
    await db.messages.create_index("created_at")

    await db.notifications.create_index("user_id")
    await db.notifications.create_index("read")
    await db.notifications.create_index("created_at")

    await db.reviews.create_index("target_id")
    await db.reviews.create_index("author_id")

    await db.favorites.create_index([("user_id", 1), ("target_id", 1)], unique=True)

    await db.reports.create_index("status")
    await db.admin_logs.create_index("created_at")

    await db.community_posts.create_index("category")
    await db.community_posts.create_index("city")
    await db.community_posts.create_index("author_id")
    await db.community_posts.create_index("created_at")
    await db.community_posts.create_index([("title", "text"), ("body", "text")])
    await db.community_posts.create_index([("location", "2dsphere")], sparse=True)

    await db.community_comments.create_index("post_id")
    await db.community_comments.create_index("created_at")

    await db.places.create_index("name")
    await db.places.create_index("ascii_name")
    await db.places.create_index("alt_names")
    await db.places.create_index("country")
    await db.places.create_index([("name", 1), ("country", 1)])

    await db.marketplace_listings.create_index("category")
    await db.marketplace_listings.create_index("city")
    await db.marketplace_listings.create_index("condition")
    await db.marketplace_listings.create_index("status")
    await db.marketplace_listings.create_index("price")
    await db.marketplace_listings.create_index("owner_id")
    await db.marketplace_listings.create_index("created_at")
    await db.marketplace_listings.create_index([("title", "text"), ("description", "text")])
    await db.marketplace_listings.create_index([("location", "2dsphere")], sparse=True)

    await db.housing_listings.create_index("housing_type")
    await db.housing_listings.create_index("city")
    await db.housing_listings.create_index("status")
    await db.housing_listings.create_index("deposit")
    await db.housing_listings.create_index("monthly_rent")
    await db.housing_listings.create_index("owner_id")
    await db.housing_listings.create_index("created_at")
    await db.housing_listings.create_index([("title", "text"), ("description", "text")])
    await db.housing_listings.create_index([("location", "2dsphere")], sparse=True)

    await db.auto_listings.create_index("listing_type")
    await db.auto_listings.create_index("make")
    await db.auto_listings.create_index("fuel_type")
    await db.auto_listings.create_index("transmission")
    await db.auto_listings.create_index("city")
    await db.auto_listings.create_index("status")
    await db.auto_listings.create_index("year")
    await db.auto_listings.create_index("price")
    await db.auto_listings.create_index("owner_id")
    await db.auto_listings.create_index("created_at")
    await db.auto_listings.create_index([("location", "2dsphere")], sparse=True)

    await db.route_posts.create_index("post_type")
    await db.route_posts.create_index("status")
    await db.route_posts.create_index("stop_names_lower")
    await db.route_posts.create_index("departure_at")
    await db.route_posts.create_index("owner_id")
    await db.route_posts.create_index("created_at")

    await db.cargo_posts.create_index("post_type")
    await db.cargo_posts.create_index("status")
    await db.cargo_posts.create_index("origin_country")
    await db.cargo_posts.create_index("destination_country")
    await db.cargo_posts.create_index("stop_names_lower")
    await db.cargo_posts.create_index("departure_at")
    await db.cargo_posts.create_index("owner_id")
    await db.cargo_posts.create_index("created_at")
