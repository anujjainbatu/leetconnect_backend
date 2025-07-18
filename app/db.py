   # MongoDB client (Motor)

import motor.motor_asyncio
from .config import settings
import ssl

# Create SSL context for serverless environments
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def create_database_connection():
    """Create a fresh database connection for each operation"""
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.MONGODB_URI,
        maxPoolSize=1,
        minPoolSize=0,
        maxIdleTimeMS=30000,
        serverSelectionTimeoutMS=10000,
        socketTimeoutMS=10000,
        connectTimeoutMS=10000,
        tls=True,
        tlsAllowInvalidCertificates=True,
        tlsAllowInvalidHostnames=True,
        retryWrites=True,
    )
    return client[settings.MONGODB_DB]

def get_database():
    """Get database connection - creates fresh connection every time"""
    return create_database_connection()



async def ensure_indexes():
    # Unique index on users.email
    db = get_database()
    try:
        await db.users.create_index("email", unique=True)
        # Compound index on leaderboard filters + score
        await db.leaderboard.create_index([("branch", 1), ("year", 1), ("score", -1)])
    except Exception:
        # Ignore index creation errors (they might already exist)
        pass
