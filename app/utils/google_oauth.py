from google.oauth2 import id_token
from google.auth.transport import requests
from ..config import settings

async def verify_google_token(id_token_str: str) -> dict:
    """
    Verify the Google ID token and ensure the email domain matches ALLOWED_DOMAIN.
    Raises ValueError if invalid or wrong domain.
    """
    info = id_token.verify_oauth2_token(
        id_token_str,
        requests.Request(),
        settings.GOOGLE_CLIENT_ID
    )
    domain = info.get("hd")
    if domain != settings.ALLOWED_DOMAIN:
        raise ValueError("Unauthorized domain")
    return info
