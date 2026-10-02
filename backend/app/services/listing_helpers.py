from typing import Any

from app.core.exceptions import ForbiddenError
from app.models.user import UserRole


def owner_summary(user: dict[str, Any]) -> dict[str, Any]:
    return {"_id": user["_id"], "name": user["name"], "avatar": user.get("avatar")}


def assert_can_modify(item: dict[str, Any], user: dict[str, Any], owner_field: str = "owner_id") -> None:
    is_owner = item[owner_field] == user["_id"]
    is_admin = UserRole.ADMIN.value in user.get("roles", [])
    if not (is_owner or is_admin):
        raise ForbiddenError("You can only modify your own listings")
