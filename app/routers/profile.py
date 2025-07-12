# app/routers/profile.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models.user import User
from ..crud.user import get_user_by_email, update_leetcode_username
from ..routers.auth import get_current_user_email

router = APIRouter(prefix="/user", tags=["user"])

class LeetCodeHandle(BaseModel):
    username: str

@router.get("/me", response_model=User)
async def read_own_profile(email: str = Depends(get_current_user_email)):
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.post("/me/leetcode", response_model=User)
async def set_leetcode_handle(
    payload: LeetCodeHandle,
    email: str = Depends(get_current_user_email)
):
    return await update_leetcode_username(email, payload.username)
