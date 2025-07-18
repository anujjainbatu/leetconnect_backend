# User-related Pydantic schemas for request/response models
from pydantic import BaseModel, EmailStr
from typing import Optional, Union

class UserResponse(BaseModel):
    """Response model for user data"""
    email: EmailStr
    name: str
    branch: Optional[str] = None
    year: Optional[Union[int, str]] = None
    leetcode_username: Optional[str] = None

class UserUpdate(BaseModel):
    """Model for updating user data"""
    name: Optional[str] = None
    leetcode_username: Optional[str] = None
