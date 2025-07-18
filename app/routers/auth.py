from fastapi import APIRouter, HTTPException, Depends
from ..schemas.auth import SignUpRequest, SignInRequest, TokenResponse, GoogleAuthRequest
from ..utils.google_oauth import verify_google_token
from ..utils.email_parse import parse_branch_year
from ..crud.user import (
    get_user_by_email,
    create_user,
    create_user_manual,
    authenticate_manual,
)
from ..models.user import User
from ..config import settings
import jwt
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid or expired token")
# —————————————
# Google OAuth (existing)
@router.post("/google", response_model=TokenResponse)
async def google_login(req: GoogleAuthRequest):
    try:
        logger.info(f"Attempting Google login with token: {req.id_token[:50]}...")
        info = await verify_google_token(req.id_token)
        logger.info(f"Google verification successful for email: {info.get('email')}")
    except ValueError as e:
        logger.error(f"Google verification failed with ValueError: {str(e)}")
        raise HTTPException(401, f"Unauthorized: {str(e)}")
    except Exception as e:
        logger.error(f"Google verification failed with exception: {str(e)}")
        raise HTTPException(401, f"Invalid token: {str(e)}")

    email = info["email"]
    user = await get_user_by_email(email)
    if not user:
        branch, year = parse_branch_year(email)
        # Get name from Google token, fallback to email if not available
        name = info.get("name", email.split("@")[0])
        user = await create_user(User(
            email=email,
            name=name,
            branch=branch,
            year=year
        ))
    token = jwt.encode({"sub": email}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return TokenResponse(access_token=token)

# Debug endpoint to test Google token verification
@router.post("/debug-google")
async def debug_google_token(req: GoogleAuthRequest):
    """Debug endpoint to test Google token verification"""
    try:
        logger.info(f"Debug: Attempting to verify Google token: {req.id_token[:50]}...")
        logger.info(f"Debug: Using Google Client ID: {settings.GOOGLE_CLIENT_ID}")
        logger.info(f"Debug: Allowed domain: {settings.ALLOWED_DOMAIN}")
        
        info = await verify_google_token(req.id_token)
        logger.info(f"Debug: Token verification successful!")
        
        return {
            "success": True,
            "user_info": info,
            "message": "Token verification successful"
        }
    except ValueError as e:
        logger.error(f"Debug: ValueError during token verification: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "ValueError"
        }
    except Exception as e:
        logger.error(f"Debug: Exception during token verification: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

# —————————————
# Manual Sign‑Up
@router.post("/signup", response_model=TokenResponse)
async def manual_signup(req: SignUpRequest):
    # Enforce domain
    domain = req.email.split("@")[-1]
    if domain != settings.ALLOWED_DOMAIN:
        raise HTTPException(401, "Email domain not allowed")

    existing = await get_user_by_email(req.email)
    if existing:
        raise HTTPException(400, "User already exists")

    branch, year = parse_branch_year(req.email)
    user = await create_user_manual(req.email, req.name, req.password, branch, year)

    token = jwt.encode({"sub": req.email}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return TokenResponse(access_token=token)

# —————————————
# Manual Sign‑In
@router.post("/login", response_model=TokenResponse)
async def manual_login(req: SignInRequest):
    user = await authenticate_manual(req.email, req.password)
    if not user:
        raise HTTPException(401, "Invalid email or password")

    token = jwt.encode({"sub": req.email}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return TokenResponse(access_token=token)
