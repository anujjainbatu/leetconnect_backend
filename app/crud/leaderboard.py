# app/crud/leaderboard.py
from typing import List
from ..db import get_database
from ..schemas.leaderboard import LeaderboardEntry, FilterParams

async def fetch_leaderboard(params: FilterParams, current_user_email: str) -> List[LeaderboardEntry]:
    db = get_database()
    query = {}
    if params.branch:
        query["branch"] = params.branch
    if params.year:
        query["year"] = params.year

    cursor = db.leaderboard.find(query).sort("score", -1).limit(100)
    results = []
    async for doc in cursor:
        # mark is_friend if this doc.username matches current_user's friends list
        is_friend = await db.users.find_one({
            "email": current_user_email,
            "friends": doc["username"]
        }) is not None
        results.append(LeaderboardEntry(
            username=doc["username"],
            score=doc["score"],
            branch=doc.get("branch"),
            year=doc.get("year"),
            is_friend=is_friend
        ))
    return results
