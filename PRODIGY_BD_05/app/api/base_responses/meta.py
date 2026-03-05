from pydantic import BaseModel
from typing import Optional


class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool


class VersionMeta(BaseModel):
    deprecated: bool
    sunset: Optional[str] = None
    link: Optional[str] = None


class Meta(BaseModel):
    pagination: Optional[PaginationMeta] = None
    version: Optional[VersionMeta] = None