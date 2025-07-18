from google.oauth2 import id_token
from google.auth.transport import requests
from ..config import settings
import logging

logger = logging.getLogger(__name__)

async def verify_google_token(id_token_str: str) -> dict:
    """
    Verify the Google ID token and ensure the email domain matches ALLOWED_DOMAIN.
    Raises ValueError if invalid or wrong domain.
    """
    try:
        logger.info(f"Verifying Google token with client ID: {settings.GOOGLE_CLIENT_ID}")
        info = id_token.verify_oauth2_token(
            id_token_str,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        logger.info(f"Token verified successfully. User info: {info}")
        
        # Check if the email domain matches the allowed domain
        email = info.get("email", "")
        domain = email.split("@")[-1] if "@" in email else ""
        
        # Also check the 'hd' field if present (hosted domain)
        hosted_domain = info.get("hd")
        
        logger.info(f"Email: {email}, Domain: {domain}, Hosted Domain: {hosted_domain}")
        
        # Allow if either the email domain matches or the hosted domain matches
        if domain != settings.ALLOWED_DOMAIN and hosted_domain != settings.ALLOWED_DOMAIN:
            logger.warning(f"Domain mismatch. Email domain: {domain}, Hosted domain: {hosted_domain}, Allowed: {settings.ALLOWED_DOMAIN}")
            raise ValueError("Unauthorized domain")
        
        return info
    except Exception as e:
        logger.error(f"Google token verification failed: {str(e)}")
        raise
