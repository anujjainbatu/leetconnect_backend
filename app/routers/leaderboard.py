# app/routers/leaderboard.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..schemas.leaderboard import LeaderboardEntry, FilterParams
from ..crud.leaderboard import fetch_leaderboard
from ..routers.auth import get_current_user_email

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/", response_model=List[LeaderboardEntry])
async def list_all(current_user: str = Depends(get_current_user_email)):
    return await fetch_leaderboard(FilterParams(), current_user)

@router.post("/filter", response_model=List[LeaderboardEntry])
async def filtered(params: FilterParams, current_user: str = Depends(get_current_user_email)):
    return await fetch_leaderboard(params, current_user)
