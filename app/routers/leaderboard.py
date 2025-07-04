 # `/leaderboard`, `/leaderboard/filter`

from fastapi import APIRouter, Depends, HTTPException
from ..schemas.leaderboard import LeaderboardEntry, FilterParams
from ..crud.leaderboard import fetch_leaderboard
from ..config import settings
import jwt

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

def get_current_user(token: str = Depends(...)) -> str:
    """
    Decode JWT, return the user’s email, or raise 401 if invalid.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid token")

@router.get("/", response_model=list[LeaderboardEntry])
async def list_all(current_user: str = Depends(get_current_user)):
    # Unfiltered leaderboard
    return await fetch_leaderboard(FilterParams(), current_user)

@router.post("/filter", response_model=list[LeaderboardEntry])
async def filtered(params: FilterParams, current_user: str = Depends(get_current_user)):
    # Branch/year filtered leaderboard
    return await fetch_leaderboard(params, current_user)
