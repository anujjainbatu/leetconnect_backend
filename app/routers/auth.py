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
