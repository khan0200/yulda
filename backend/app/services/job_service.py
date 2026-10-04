from datetime import datetime, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobPostCreate, JobPostUpdate
from app.services.listing_helpers import assert_can_modify, owner_summary


class JobService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = JobRepository(db)

    async def create_post(self, owner: dict[str, Any], payload: JobPostCreate) -> dict[str, Any]:
        doc = payload.model_dump()
        if doc.get("location"):
            doc["location"] = payload.location.model_dump()
        doc["owner_id"] = owner["_id"]
        doc["owner"] = owner_summary(owner)
        return await self._repo.create(doc)

    async def get_post(self, job_id: str) -> dict[str, Any]:
        post = await self._repo.find_by_id(job_id)
        if not post:
            raise NotFoundError("Job post not found")
        return post

    async def list_posts(
        self,
        post_type: str | None,
        category: str | None,
        employment_type: str | None,
        city: str | None,
        requires_korean: bool | None,
        visa_sponsorship: bool | None,
        accepted_visa: str | None,
        housing_option: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list(
            post_type=post_type,
            category=category,
            employment_type=employment_type,
            city=city,
            requires_korean=requires_korean,
            visa_sponsorship=visa_sponsorship,
            accepted_visa=accepted_visa,
            housing_option=housing_option,
            page=page,
            page_size=page_size,
        )

    async def update_post(self, job_id: str, user: dict[str, Any], payload: JobPostUpdate) -> dict[str, Any]:
        post = await self.get_post(job_id)
        assert_can_modify(post, user)
        updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
        updated = await self._repo.update(post["_id"], updates)
        assert updated is not None
        return updated

    async def delete_post(self, job_id: str, user: dict[str, Any]) -> None:
        post = await self.get_post(job_id)
        assert_can_modify(post, user)
        await self._repo.delete(post["_id"])

    async def list_my_posts(self, user: dict[str, Any], page: int, page_size: int) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list_by_owner(user["_id"], page=page, page_size=page_size)

    async def repost_post(self, job_id: str, user: dict[str, Any]) -> dict[str, Any]:
        post = await self.get_post(job_id)
        assert_can_modify(post, user)
        now = datetime.now(timezone.utc)
        updated = await self._repo.update(post["_id"], {"created_at": now, "status": "ACTIVE"})
        assert updated is not None
        return updated
