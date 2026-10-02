import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from app.core.config import settings

logger = logging.getLogger("yulda.database")

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
