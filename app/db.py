   # MongoDB client (Motor)

import motor.motor_asyncio
from .config import settings

# Initialize Motor (async MongoDB) client
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)

# Use default database from the URI
db = client.get_default_database()
