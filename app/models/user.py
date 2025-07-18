# Pydantic + Mongo schema for users
from pydantic import BaseModel, EmailStr
from typing import Optional, Union

class User(BaseModel):
    # User's email (must be valid)
    email: EmailStr
    # Display name from Google profile
    name: str
    # Parsed branch & year (e.g. "cs" and "22")
    branch: Optional[str] = None
    year: Optional[Union[int, str]] = None
    # LeetCode username (provided by user)
    leetcode_username: Optional[str] = None
    # Only populated for manual signup users
    hashed_password: Optional[str] = None
