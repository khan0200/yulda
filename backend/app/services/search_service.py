from __future__ import annotations

import re
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

_RESULT_LIMIT = 5


class SearchService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db

    async def search(self, query: str) -> dict[str, list[dict[str, Any]]]:
        trimmed = query.strip()
        if not trimmed:
            return {"marketplace": [], "community": []}

        pattern = re.compile(re.escape(trimmed), re.IGNORECASE)

        marketplace_cursor = (
            self._db.marketplace_listings.find(
                {
                    "status": "ACTIVE",
                    "$or": [{"title": pattern}, {"description": pattern}],
                }
            )
            .sort("created_at", -1)
            .limit(_RESULT_LIMIT)
        )
        community_cursor = (
            self._db.community_posts.find(
                {"$or": [{"title": pattern}, {"body": pattern}]}
            )
            .sort("created_at", -1)
            .limit(_RESULT_LIMIT)
        )

        marketplace_items = await marketplace_cursor.to_list(length=_RESULT_LIMIT)
        community_items = await community_cursor.to_list(length=_RESULT_LIMIT)

        return {"marketplace": marketplace_items, "community": community_items}
