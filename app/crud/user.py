 # create/get user, filter by domain, etc.

from ..db import db
from ..models.user import User
from typing import Optional
from ..utils.security import hash_password, verify_password

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



async def create_user_manual(email: str, name: str, password: str, branch: str, year: str):
    """Create a user with a hashed password."""
    hashed = hash_password(password)
    user = {"email": email, "name": name, "branch": branch, "year": year, "hashed_password": hashed}
    await db.users.insert_one(user)
    return user

async def authenticate_manual(email: str, password: str):
    """
    Return user dict if password matches, else None.
    """
    user = await db.users.find_one({"email": email})
    if not user or not user.get("hashed_password"):
        return None
    if verify_password(password, user["hashed_password"]):
        return user
    return None
