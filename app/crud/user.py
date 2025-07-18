 # create/get user, filter by domain, etc.

from ..db import get_database
from ..models.user import User
from typing import Optional
from ..utils.security import hash_password, verify_password

async def get_user_by_email(email: str) -> Optional[User]:
    # Fetch a user document by email
    try:
        db = get_database()
        data = await db.users.find_one({"email": email})
        return User(**data) if data else None
    except Exception as e:
        # Log the error and return None to indicate user not found
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching user by email {email}: {str(e)}")
        return None

async def create_user(user: User):
    # Insert new user document
    db = get_database()
    await db.users.insert_one(user.model_dump())
    return user

async def create_user_manual(email: str, name: str, password: str, branch: str, year: str):
    """Create a user with a hashed password."""
    hashed = hash_password(password)
    user_doc = {
        "email": email, 
        "name": name,
        "branch": branch, 
        "year": year,
        "hashed_password": hashed,
        "leetcode_username": None,
        "friends": []
    }
    db = get_database()
    await db.users.insert_one(user_doc)
    return User(**user_doc)

async def authenticate_manual(email: str, password: str):
    """
    Return user dict if password matches, else None.
    """
    db = get_database()
    user = await db.users.find_one({"email": email})
    if not user or not user.get("hashed_password"):
        return None
    if verify_password(password, user["hashed_password"]):
        return user
    return None

async def update_leetcode_username(email: str, handle: str) -> User:
    # set the field on the MongoDB document
    db = get_database()
    await db.users.update_one({"email": email}, {"$set": {"leetcode_username": handle}})
    doc = await db.users.find_one({"email": email})
    return User(**doc)