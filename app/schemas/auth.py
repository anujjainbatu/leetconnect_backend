# UserIn, UserOut

from pydantic import BaseModel, EmailStr, Field

class GoogleAuthRequest(BaseModel):
    # ID token obtained from Google Sign‑In
    id_token: str

class TokenResponse(BaseModel):
    # JWT issued on successful login
    access_token: str
    # Always “bearer”
    token_type: str = "bearer"


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str

class SignInRequest(BaseModel):
    email: EmailStr
    password: str
