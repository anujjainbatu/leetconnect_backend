from pydantic import BaseSettings

class Settings(BaseSettings):
    # MongoDB connection string
    MONGODB_URI: str
    # Google OAuth client ID for verifying tokens
    GOOGLE_CLIENT_ID: str
    # Only allow users from this domain to sign in
    ALLOWED_DOMAIN: str = "satiengg.in"
    # JWT secret and algorithm for token generation
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        # Load variables from .env in project root
        env_file = ".env"

# Instantiate once and reuse
settings = Settings()
