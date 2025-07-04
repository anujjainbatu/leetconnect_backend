# UserIn, UserOut

from pydantic import BaseModel

class GoogleAuthRequest(BaseModel):
    # ID token obtained from Google Sign‑In
    id_token: str

class TokenResponse(BaseModel):
    # JWT issued on successful login
    access_token: str
    # Always “bearer”
    token_type: str = "bearer"
