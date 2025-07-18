from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from pathlib import Path

# Only load .env file if it exists (for local development)
HERE = Path(__file__).parent.parent
env_file = HERE / ".env"
if env_file.exists():
    load_dotenv(env_file, override=True)

class Settings(BaseSettings):
    # MongoDB connection string
    MONGODB_URI: str
    # MongoDB db name string
    MONGODB_DB: str
    # Google OAuth client ID for verifying tokens
    GOOGLE_CLIENT_ID: str
    # Only allow users from this domain to sign in
    ALLOWED_DOMAIN: str = "satiengg.in"
    # JWT secret and algorithm for token generation
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        # This will load from environment variables in production
        env_file = None
        case_sensitive = True

# Instantiate once and reuse
settings = Settings()

# Debug print
# print("🔑 Loaded MONGODB_URI =", settings.MONGODB_URI)
# print("🔑 Loaded MONGODB_DB  =", settings.MONGODB_DB)