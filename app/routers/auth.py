# `/auth/google` callback, issue JWT

from fastapi import APIRouter, HTTPException
from ..schemas.auth import GoogleAuthRequest, TokenResponse
from ..utils.google_oauth import verify_google_token
from ..crud.user import get_user_by_email, create_user
from ..models.user import User
from ..utils.email_parse import parse_branch_year
from ..config import settings
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/google", response_model=TokenResponse)
async def google_login(req: GoogleAuthRequest):
    """
    1) Verify Google ID token & domain
    2) Create user if new, parsing branch/year
    3) Issue JWT for session
    """
    try:
        info = await verify_google_token(req.id_token)
    except Exception:
        raise HTTPException(401, "Invalid token or unauthorized domain")

    email = info["email"]
    user = await get_user_by_email(email)
    if not user:
        branch, year = parse_branch_year(email)
        user = await create_user(User(
            email=email,
            name=info["name"],
            branch=branch,
            year=year
        ))
    token = jwt.encode({"sub": email}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return TokenResponse(access_token=token)
