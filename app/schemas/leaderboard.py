from pydantic import BaseModel
from typing import Optional

class LeaderboardEntry(BaseModel):
    # LeetCode username
    username: str
    # Numeric score (e.g. problems solved)
    score: int
    # Branch & year for filtering
    branch: Optional[str]
    year: Optional[str]
    # Whether current user has friended this entry
    is_friend: bool

class FilterParams(BaseModel):
    # Optional branch filter (e.g. "cs")
    branch: Optional[str]
    # Optional year filter (e.g. "22")
    year: Optional[str]
