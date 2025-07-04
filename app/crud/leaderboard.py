 # fetch top N, filter by branch/year, etc.

from ..db import db
from ..schemas.leaderboard import LeaderboardEntry, FilterParams
from typing import List

async def fetch_leaderboard(params: FilterParams, current_user_email: str) -> List[LeaderboardEntry]:
    """
    Query the `leaderboard` collection, apply optional branch/year filters,
    sort by score descending, and mark entries as friends if present.
    """
    query = {}
    if params.branch:
        query["branch"] = params.branch
    if params.year:
        query["year"] = params.year

    cursor = db.leaderboard.find(query).sort("score", -1).limit(100)
    results = []
    async for doc in cursor:
        is_friend = await db.users.find_one({
            "email": current_user_email,
            "friends": doc["username"]
        }) is not None
        results.append(LeaderboardEntry(**doc, is_friend=is_friend))
    return results
