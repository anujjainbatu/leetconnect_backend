   # MongoDB client (Motor)

import motor.motor_asyncio
from .config import settings
import ssl

# Create SSL context for serverless environments
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Initialize Motor (async MongoDB) client with serverless-friendly settings
client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.MONGODB_URI,
    maxPoolSize=1,  # Limit connection pool for serverless
    minPoolSize=0,  # Allow connections to be closed
    maxIdleTimeMS=30000,  # Close idle connections after 30 seconds
    serverSelectionTimeoutMS=10000,  # 10 second timeout
    socketTimeoutMS=10000,  # 10 second socket timeout
    connectTimeoutMS=10000,  # 10 second connection timeout
    tls=True,  # Enable TLS
    tlsAllowInvalidCertificates=True,  # Allow invalid certificates for serverless
    tlsAllowInvalidHostnames=True,  # Allow invalid hostnames for serverless
    retryWrites=True,  # Enable retryable writes
)

# 🎯 Explicitly pick the DB name
db = client[settings.MONGODB_DB]



async def ensure_indexes():
    # Unique index on users.email
    await db.users.create_index("email", unique=True)
    # Compound index on leaderboard filters + score
    await db.leaderboard.create_index([("branch", 1), ("year", 1), ("score", -1)])
