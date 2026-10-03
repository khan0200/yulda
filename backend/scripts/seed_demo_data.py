"""Seed each marketplace-style page with 20 realistic demo listings.

Run from backend/ with: ./.venv/Scripts/python.exe scripts/seed_demo_data.py
Safe to re-run — it skips creation for any user that already exists,
but will always add a fresh batch of listings.
"""

import asyncio
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import connect_to_mongo, close_mongo_connection, get_database  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auto_service import AutoService  # noqa: E402
from app.services.cargo_service import CargoService  # noqa: E402
from app.services.community_service import CommunityService  # noqa: E402
from app.services.housing_service import HousingService  # noqa: E402
from app.services.job_service import JobService  # noqa: E402
from app.services.marketplace_service import MarketplaceService  # noqa: E402
from app.services.route_service import RouteService  # noqa: E402
from app.services.service_service import ServicePostService  # noqa: E402

from app.schemas.auto import AutoListingCreate  # noqa: E402
from app.schemas.cargo import CargoPostCreate  # noqa: E402
from app.schemas.community import PostCreate  # noqa: E402
from app.schemas.housing import HousingCreate  # noqa: E402
from app.schemas.job import JobPostCreate  # noqa: E402
from app.schemas.marketplace import ListingCreate  # noqa: E402
from app.schemas.route import RoutePostCreate  # noqa: E402
from app.schemas.service import ServicePostCreate  # noqa: E402

N = 20

DEMO_USERS = [
    {"email": "demo.aziz@yulda.test", "name": "Aziz Karimov"},
    {"email": "demo.dilnoza@yulda.test", "name": "Dilnoza Yusupova"},
    {"email": "demo.jasur@yulda.test", "name": "Jasur Toshmatov"},
    {"email": "demo.minji@yulda.test", "name": "Kim Minji"},
    {"email": "demo.sardor@yulda.test", "name": "Sardor Alimov"},
    {"email": "demo.nodira@yulda.test", "name": "Nodira Rashidova"},
    {"email": "demo.jihoon@yulda.test", "name": "Park Jihoon"},
    {"email": "demo.shoxrux@yulda.test", "name": "Shoxrux Nazarov"},
]

CITIES = ["Seoul", "Ansan", "Incheon", "Suwon", "Cheongju", "Cheonan", "Daegu", "Busan", "Gimhae", "Pyeongtaek"]
UZ_CITIES = ["Tashkent", "Samarqand", "Andijon", "Namangan", "Fergana", "Bukhara"]

UNSPLASH = lambda photo_id: f"https://images.unsplash.com/{photo_id}?w=800&q=70&auto=format&fit=crop"  # noqa: E731

PHOTOS = {
    "electronics": [UNSPLASH("photo-1511707171634-5f897ff02aa9"), UNSPLASH("photo-1498049794561-7780e7231661")],
    "furniture": [UNSPLASH("photo-1555041469-a586c61ea9bc"), UNSPLASH("photo-1586023492125-27b2c045efd7")],
    "bikes": [UNSPLASH("photo-1485965120184-e220f721d03e"), UNSPLASH("photo-1532298229144-0ec0c57515c7")],
    "clothing": [UNSPLASH("photo-1434389677669-e08b4cac3105"), UNSPLASH("photo-1489987707025-afc232f7ea0f")],
    "food": [UNSPLASH("photo-1504674900247-0877df9cc836"), UNSPLASH("photo-1540189549336-e6e99c3679fe")],
    "free": [UNSPLASH("photo-1516455590571-18256e5bb9ff")],
    "other": [UNSPLASH("photo-1586769852044-692d6e3703f2")],
    "housing": [UNSPLASH("photo-1522708323590-d24dbb6b0267"), UNSPLASH("photo-1502672260266-1c1ef2d93688"), UNSPLASH("photo-1493809842364-78817add7ffb")],
    "auto": [UNSPLASH("photo-1503376780353-7e6692767b70"), UNSPLASH("photo-1552519507-da3b142c6e3d"), UNSPLASH("photo-1511919884226-fd3cad34687c")],
    "jobs": [UNSPLASH("photo-1521737604893-d14cc237f11d"), UNSPLASH("photo-1556761175-5973dc0f32e7")],
    "services_beauty": [UNSPLASH("photo-1560066984-138dadb4c035")],
    "services_repair": [UNSPLASH("photo-1581092160562-40aa08e78837")],
    "services_tutoring": [UNSPLASH("photo-1503676260728-1c00da094a0b")],
    "services_cleaning": [UNSPLASH("photo-1581578731548-c64695cc6952")],
    "services_other": [UNSPLASH("photo-1521791136064-7986c2920216")],
    "community": [UNSPLASH("photo-1517457373958-b7bdd4587205")],
}


def rand_photos(key: str, n: int = 1) -> list[str]:
    pool = PHOTOS.get(key, PHOTOS["other"])
    return random.sample(pool, k=min(n, len(pool)))


async def ensure_users(db) -> list[dict]:
    repo = UserRepository(db)
    users = []
    for u in DEMO_USERS:
        existing = await repo.find_by_email(u["email"])
        if existing:
            users.append(existing)
            continue
        doc = {
            "email": u["email"],
            "phone": None,
            "password_hash": hash_password("DemoPass123!"),
            "name": u["name"],
            "avatar": None,
            "roles": ["USER"],
            "verification_status": "UNVERIFIED",
            "location": None,
        }
        created = await repo.create(doc)
        users.append(created)
    return users


def pick_user(users):
    return random.choice(users)


async def seed_marketplace(db, users):
    service = MarketplaceService(db)
    categories = ["ELECTRONICS", "FURNITURE", "BIKES", "CLOTHING", "FOOD", "FREE", "OTHER"]
    items = [
        ("iPhone 13 Pro 256GB", "Battery 89%, minor scratches on back", 650000, "ELECTRONICS", "USED"),
        ("Samsung Galaxy S23", "Like new, box included", 850000, "ELECTRONICS", "USED"),
        ("MacBook Air M1", "Barely used, 8GB/256GB", 1100000, "ELECTRONICS", "USED"),
        ("Sony WH-1000XM4 headphones", "Great noise cancelling, all accessories", 180000, "ELECTRONICS", "USED"),
        ("iPad 9th gen", "64GB WiFi, with case", 320000, "ELECTRONICS", "USED"),
        ("IKEA 2-seater sofa", "Grey fabric, pickup only", 150000, "FURNITURE", "USED"),
        ("Study desk + chair set", "Good for students, minor wear", 90000, "FURNITURE", "USED"),
        ("Queen size mattress", "6 months old, very clean", 200000, "FURNITURE", "USED"),
        ("Bookshelf 5-tier", "Solid wood, sturdy", 60000, "FURNITURE", "USED"),
        ("Mountain bike 27-speed", "Trek, recently serviced", 280000, "BIKES", "USED"),
        ("Folding city bike", "Lightweight, great for commuting", 150000, "BIKES", "USED"),
        ("Kids bicycle 16 inch", "Barely used, with training wheels", 55000, "BIKES", "USED"),
        ("Winter jacket North Face", "Size L, warm and waterproof", 120000, "CLOTHING", "USED"),
        ("Designer handbag", "Authentic, comes with receipt", 300000, "CLOTHING", "NEW"),
        ("Running shoes Nike 270", "Size 270mm, worn twice", 70000, "CLOTHING", "USED"),
        ("Rice cooker Cuckoo 6-cup", "Works perfectly, moving out sale", 45000, "FOOD", "USED"),
        ("Unopened instant noodles box", "30 packs, moving out", 0, "FREE", "NEW"),
        ("Free moving boxes", "20+ boxes, various sizes", 0, "FREE", "USED"),
        ("Electric kettle", "Used a few times only", 15000, "OTHER", "USED"),
        ("Desk lamp LED", "Adjustable brightness, like new", 20000, "OTHER", "USED"),
    ]
    for title, desc, price, category, condition in items:
        owner = pick_user(users)
        photo_key = category.lower() if category.lower() in PHOTOS else "other"
        payload = ListingCreate(
            category=category,
            title=title,
            description=desc,
            price=price,
            condition=condition,
            photos=rand_photos(photo_key, 1),
            city=random.choice(CITIES),
            contact_method=random.choice(["PHONE", "CHAT", "KAKAOTALK"]),
            contact_value="010-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999)),
        )
        await service.create_listing(owner, payload)
    print(f"  marketplace: {len(items)} listings")


async def seed_housing(db, users):
    service = HousingService(db)
    types = ["ONE_ROOM", "TWO_ROOM", "ROOMMATE", "APARTMENT", "COMMERCIAL"]
    titles = [
        "Cozy one-room near subway station", "Bright studio with balcony", "Newly renovated 2-room apt",
        "Roommate wanted for shared flat", "Modern apartment near university", "Quiet one-room, pet-friendly",
        "Spacious 2-room with parking", "Studio with rooftop access", "Shared house, 2 rooms available",
        "Officetel near Gangnam", "Budget one-room for students", "Family apartment 3 bedrooms",
        "Renovated commercial space downtown", "One-room with full furniture", "Two-room near park",
        "Studio close to factory area", "Clean roommate share, female only", "Apartment with elevator",
        "One-room, move-in ready", "Townhouse with small yard",
    ]
    for i, title in enumerate(titles):
        owner = pick_user(users)
        deposit = random.choice([2000000, 5000000, 10000000, 20000000])
        rent = random.choice([350000, 450000, 550000, 700000])
        payload = HousingCreate(
            housing_type=types[i % len(types)],
            title=title,
            description=f"{title}. Clean and well-maintained, close to transit and convenience stores.",
            deposit=deposit,
            monthly_rent=rent,
            maintenance_fee=random.choice([0, 50000, 80000]),
            amenities=random.sample(["FRIDGE", "WASHER", "AC", "PARKING", "TV", "ELEVATOR", "INTERNET"], k=3),
            photos=rand_photos("housing", 1),
            city=random.choice(CITIES),
            metro_station=random.choice(["Gangnam", "Hongdae", "Sadang", None]),
            contact_value="010-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999)),
            area_m2=round(random.uniform(18, 60), 1),
            room_count=random.choice([1, 1, 2, 3]),
            floor=random.randint(1, 15),
            total_floors=random.randint(5, 20),
            building_year=random.randint(2005, 2023),
            direction=random.choice(["SOUTH", "SOUTHEAST", "EAST", "NORTH", None]),
        )
        await service.create_listing(owner, payload)
    print(f"  housing: {len(titles)} listings")


async def seed_auto(db, users):
    service = AutoService(db)
    cars = [
        ("Hyundai", "Avante", 2020), ("Hyundai", "Sonata", 2019), ("Kia", "K5", 2021),
        ("Kia", "Sportage", 2020), ("Kia", "Morning", 2018), ("Genesis", "G70", 2021),
        ("Chevrolet", "Spark", 2017), ("KGM", "Tivoli", 2019), ("BMW", "3 Series", 2020),
        ("Mercedes-Benz", "C-Class", 2019), ("Tesla", "Model 3", 2022), ("Toyota", "Camry", 2020),
        ("Hyundai", "Tucson", 2021), ("Kia", "Seltos", 2022), ("Hyundai", "Santa Fe", 2019),
        ("Kia", "Carnival", 2020), ("Renault", "XM3", 2021), ("Hyundai", "Ioniq 5", 2023),
        ("Kia", "EV6", 2023), ("Volkswagen", "Golf", 2018),
    ]
    body_types = ["SEDAN", "SUV", "HATCHBACK", "MINIVAN", "WAGON"]
    for make, model, year in cars:
        owner = pick_user(users)
        listing_type = random.choice(["SALE", "SALE", "SALE", "RENTAL"])
        price = random.randint(8_000_000, 45_000_000)
        payload = AutoListingCreate(
            listing_type=listing_type,
            make=make,
            model=model,
            year=year,
            mileage_km=random.randint(5000, 150000),
            fuel_type=random.choice(["GASOLINE", "DIESEL", "HYBRID", "ELECTRIC"]),
            transmission=random.choice(["AUTOMATIC", "MANUAL"]),
            price=price,
            rental_price_per_day=random.randint(50000, 150000) if listing_type == "RENTAL" else None,
            description=f"{year} {make} {model}, well maintained, regular service history.",
            photos=rand_photos("auto", 1),
            city=random.choice(CITIES),
            contact_value="010-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999)),
            body_type=random.choice(body_types),
            color=random.choice(["White", "Black", "Silver", "Gray", "Blue"]),
            accident_history=random.choice(["NONE", "NONE", "MINOR"]),
            owner_count=random.randint(1, 3),
            credit_available=random.choice([True, False]),
        )
        await service.create_listing(owner, payload)
    print(f"  auto: {len(cars)} listings")


async def seed_jobs(db, users):
    service = JobService(db)
    jobs = [
        ("Kitchen helper needed evenings", "RESTAURANT_CAFE", "PART_TIME", "OFFER"),
        ("Cafe barista wanted", "RESTAURANT_CAFE", "PART_TIME", "OFFER"),
        ("Store clerk, weekends", "RETAIL", "PART_TIME", "OFFER"),
        ("Warehouse packing staff", "DELIVERY_LOGISTICS", "FULL_TIME", "OFFER"),
        ("Delivery driver (own car)", "DELIVERY_LOGISTICS", "DAILY", "OFFER"),
        ("Factory line worker", "CONSTRUCTION_FACTORY", "FULL_TIME", "OFFER"),
        ("Construction site helper", "CONSTRUCTION_FACTORY", "DAILY", "OFFER"),
        ("House cleaning staff needed", "CLEANING", "PART_TIME", "OFFER"),
        ("Office cleaner, early morning", "CLEANING", "PART_TIME", "OFFER"),
        ("Babysitter needed on weekends", "CARE_CHILDCARE", "PART_TIME", "OFFER"),
        ("Elderly care assistant", "CARE_CHILDCARE", "FULL_TIME", "OFFER"),
        ("Office admin assistant", "OFFICE_ADMIN", "FULL_TIME", "OFFER"),
        ("Frontend developer (contract)", "IT_DESIGN", "CONTRACT", "OFFER"),
        ("Graphic designer needed", "IT_DESIGN", "PART_TIME", "OFFER"),
        ("Korean tutor for beginners", "EDUCATION_TUTORING", "PART_TIME", "OFFER"),
        ("Uzbek-Korean translator needed", "TRANSLATION", "PER_PROJECT" if False else "CONTRACT", "OFFER"),
        ("Event staff for weekend festival", "EVENT_PROMOTION", "DAILY", "OFFER"),
        ("Looking for kitchen work", "RESTAURANT_CAFE", "PART_TIME", "REQUEST"),
        ("Looking for factory job, available immediately", "CONSTRUCTION_FACTORY", "FULL_TIME", "REQUEST"),
        ("Experienced cleaner looking for work", "CLEANING", "PART_TIME", "REQUEST"),
    ]
    for title, category, emp_type, post_type in jobs:
        owner = pick_user(users)
        payload = JobPostCreate(
            post_type=post_type,
            category=category,
            employment_type=emp_type,
            title=title,
            description=f"{title}. Flexible schedule, friendly team, details on contact.",
            pay_type=random.choice(["HOURLY", "DAILY", "MONTHLY"]),
            pay_amount=random.choice([10000, 11000, 12000, 2500000, 80000]),
            city=random.choice(CITIES),
            requires_korean=random.choice([True, False, False]),
            visa_sponsorship=random.choice([True, False, False]),
            photos=rand_photos("jobs", 1) if random.random() > 0.5 else [],
            contact_value="010-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999)),
        )
        await service.create_post(owner, payload)
    print(f"  jobs: {len(jobs)} listings")


async def seed_services(db, users):
    service = ServicePostService(db)
    items = [
        ("Haircut at your home", "BEAUTY", "20000 won"),
        ("Nail art and manicure", "BEAUTY", "25000 won"),
        ("Phone screen repair, same day", "REPAIR", "40000 won"),
        ("Laptop repair and cleaning", "REPAIR", "negotiable"),
        ("Korean language tutoring", "TUTORING", "15000 won/hour"),
        ("Math tutoring for middle school", "TUTORING", "20000 won/hour"),
        ("Deep house cleaning", "CLEANING", "80000 won"),
        ("Office cleaning service", "CLEANING", "negotiable"),
        ("Moving help with truck", "MOVING", "150000 won"),
        ("Small moving / furniture pickup", "MOVING", "80000 won"),
        ("Dog walking and pet sitting", "PET_CARE", "10000 won/walk"),
        ("Pet grooming at home", "PET_CARE", "30000 won"),
        ("Portrait photography session", "PHOTOGRAPHY", "100000 won"),
        ("Event photography", "PHOTOGRAPHY", "negotiable"),
        ("Logo and poster design", "DESIGN", "50000 won"),
        ("Resume design and editing", "DESIGN", "30000 won"),
        ("Uzbek-Korean document translation", "TRANSLATION", "negotiable"),
        ("Visa document help", "LEGAL_ADMIN", "negotiable"),
        ("Birthday party planning", "EVENT", "negotiable"),
        ("Furniture assembly service", "OTHER", "25000 won"),
    ]
    for title, category, price_note in items:
        owner = pick_user(users)
        photo_key = f"services_{category.lower()}" if f"services_{category.lower()}" in PHOTOS else "services_other"
        payload = ServicePostCreate(
            category=category,
            title=title,
            description=f"{title}. Reliable and friendly, flexible schedule, message for details.",
            price_note=price_note,
            city=random.choice(CITIES),
            photos=rand_photos(photo_key, 1),
            contact_value="010-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999)),
        )
        await service.create_post(owner, payload)
    print(f"  services: {len(items)} listings")


async def seed_community(db, users):
    service = CommunityService(db)
    posts = [
        ("Best Uzbek restaurant near Ansan?", "QUESTION", "Looking for authentic plov and shashlik nearby."),
        ("Anyone know a good dentist?", "QUESTION", "Need a dentist who speaks English or Russian."),
        ("Community gathering this weekend", "ANNOUNCEMENT", "All Uzbek community members welcome, Saturday 3pm."),
        ("Lost wallet near subway station", "LOST_AND_FOUND", "Black leather wallet, lost yesterday evening."),
        ("Found keys near bus stop", "LOST_AND_FOUND", "Found a set of keys with a blue keychain."),
        ("Football meetup every Sunday", "MEETUP", "We play football every Sunday morning, join us!"),
        ("Language exchange meetup", "MEETUP", "Korean-Uzbek language exchange every Friday evening."),
        ("Traveling to Tashkent next month, can carry items", "TRAVELER_REQUEST", "Flying March 15, have extra luggage space."),
        ("Need someone to bring medicine from Uzbekistan", "TRAVELER_REQUEST", "Specific medicine not available here, willing to pay."),
        ("New visa regulations announced", "NEWS", "Important update on E-9 visa renewal process."),
        ("Where to buy halal meat?", "QUESTION", "Looking for a reliable halal butcher in this area."),
        ("Free Korean class starting next week", "ANNOUNCEMENT", "Free beginner Korean class, sign up required."),
        ("Lost phone at the park", "LOST_AND_FOUND", "Samsung phone with a cracked screen, lost this morning."),
        ("Weekend hiking group", "MEETUP", "Planning a hiking trip this Saturday, beginners welcome."),
        ("Does anyone know about remittance fees?", "QUESTION", "Which service has the lowest fee for sending money home?"),
        ("Community New Year celebration", "ANNOUNCEMENT", "Join us for Nowruz celebration next month."),
        ("Carrying cargo to Samarkand in April", "TRAVELER_REQUEST", "Have space for small packages, contact me."),
        ("Found a cat near the market", "LOST_AND_FOUND", "Orange tabby cat, very friendly, looking for owner."),
        ("Job fair this month", "NEWS", "Local job fair for foreign workers, details inside."),
        ("Anyone interested in forming a cricket team?", "MEETUP", "Looking for players for weekend cricket matches."),
    ]
    for title, category, body in posts:
        author = pick_user(users)
        payload = PostCreate(
            category=category,
            title=title,
            body=body,
            photos=rand_photos("community", 1) if random.random() > 0.6 else [],
            city=random.choice(CITIES),
        )
        await service.create_post(author, payload)
    print(f"  community: {len(posts)} posts")


async def seed_routes(db, users):
    service = RouteService(db)
    kr_cities = CITIES
    routes = [
        ("Seoul", "Ansan"), ("Incheon", "Suwon"), ("Ansan", "Cheonan"), ("Seoul", "Busan"),
        ("Daegu", "Busan"), ("Suwon", "Cheongju"), ("Incheon", "Seoul"), ("Gimhae", "Busan"),
        ("Pyeongtaek", "Ansan"), ("Seoul", "Incheon"), ("Cheonan", "Daegu"), ("Ansan", "Suwon"),
        ("Busan", "Gimhae"), ("Cheongju", "Seoul"), ("Seoul", "Suwon"), ("Incheon", "Ansan"),
        ("Daegu", "Seoul"), ("Suwon", "Pyeongtaek"), ("Cheonan", "Seoul"), ("Busan", "Daegu"),
    ]
    for i, (from_city, to_city) in enumerate(routes):
        owner = pick_user(users)
        post_type = random.choice(["OFFER", "OFFER", "REQUEST"])
        departure = datetime.now(timezone.utc) + timedelta(hours=random.randint(2, 72))
        payload = RoutePostCreate(
            post_type=post_type,
            stops=[{"name": from_city, "country": "KR"}, {"name": to_city, "country": "KR"}],
            departure_at=departure,
            vehicle_info=random.choice(["Hyundai Sonata", "Kia Carnival", None]) if post_type == "OFFER" else None,
            seats=random.randint(1, 3) if post_type == "OFFER" else None,
            has_cargo_space=random.choice([True, False]),
            price_note=random.choice(["15000 won", "20000 won", "negotiable"]),
            notes="Flexible on exact time, message to confirm.",
            contact_phone="010-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999)),
        )
        await service.create_post(owner, payload)
    print(f"  taxi/routes: {len(routes)} posts")


async def seed_cargo(db, users):
    service = CargoService(db)
    routes = [
        ("Incheon", "Tashkent"), ("Seoul", "Samarqand"), ("Busan", "Andijon"), ("Ansan", "Tashkent"),
        ("Cheongju", "Namangan"), ("Suwon", "Fergana"), ("Seoul", "Bukhara"), ("Incheon", "Andijon"),
        ("Daegu", "Tashkent"), ("Ansan", "Samarqand"), ("Pyeongtaek", "Tashkent"), ("Seoul", "Namangan"),
        ("Busan", "Tashkent"), ("Incheon", "Fergana"), ("Cheonan", "Tashkent"), ("Suwon", "Andijon"),
        ("Gimhae", "Tashkent"), ("Seoul", "Andijon"), ("Ansan", "Bukhara"), ("Incheon", "Samarqand"),
    ]
    categories = ["DOCUMENTS", "MEDICINE", "PERSONAL_ITEMS", "FOOD", "CLOTHING", "ELECTRONICS", "PHONE"]
    for from_city, to_city in routes:
        owner = pick_user(users)
        post_type = random.choice(["OFFER", "REQUEST"])
        departure = datetime.now(timezone.utc) + timedelta(days=random.randint(1, 14))
        payload = CargoPostCreate(
            post_type=post_type,
            stops=[{"name": from_city, "country": "KR" if from_city in CITIES else "UZ"}, {"name": to_city, "country": "KR" if to_city in CITIES else "UZ"}],
            departure_at=departure,
            accepted_categories=random.sample(categories, k=3),
            rejected_categories=[],
            max_weight_kg=random.choice([5, 10, 15, 20]),
            price_note=random.choice(["Negotiable", "5000 won/kg", "Fixed 50000 won"]),
            notes="Contact for exact pickup/drop-off arrangements.",
            contact_phone="010-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999)),
        )
        await service.create_post(owner, payload)
    print(f"  delivery/cargo: {len(routes)} posts")


async def main():
    random.seed(42)
    await connect_to_mongo()
    db = get_database()

    print("Ensuring demo users...")
    users = await ensure_users(db)
    print(f"  {len(users)} demo users ready")

    print("Seeding listings...")
    await seed_marketplace(db, users)
    await seed_housing(db, users)
    await seed_auto(db, users)
    await seed_jobs(db, users)
    await seed_services(db, users)
    await seed_community(db, users)
    await seed_routes(db, users)
    await seed_cargo(db, users)

    print("Done.")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
