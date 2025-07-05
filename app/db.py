   # MongoDB client (Motor)

import motor.motor_asyncio
from .config import settings

# Initialize Motor (async MongoDB) client
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)

# Use default database from the URI
db = client.get_default_database()



async def ensure_indexes():
    # Unique index on users.email
    await db.users.create_index("email", unique=True)
    # Compound index on leaderboard filters + score
    await db.leaderboard.create_index([("branch", 1), ("year", 1), ("score", -1)])
