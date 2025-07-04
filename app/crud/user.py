 # create/get user, filter by domain, etc.

from ..db import db
from ..models.user import User
from typing import Optional

async def get_user_by_email(email: str) -> Optional[User]:
    # Fetch a user document by email
    data = await db.users.find_one({"email": email})
    return User(**data) if data else None

async def create_user(user: User):
    # Insert new user document
    await db.users.insert_one(user.dict())
    return user

async def set_leetcode_username(email: str, lc_user: str):
    # Update the user's LeetCode username
    await db.users.update_one({"email": email}, {"$set": {"leetcode_username": lc_user}})
