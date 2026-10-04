from pydantic import BaseModel

from app.schemas.community import PostPublic
from app.schemas.marketplace import ListingPublic


class SearchResults(BaseModel):
    marketplace: list[ListingPublic]
    community: list[PostPublic]
