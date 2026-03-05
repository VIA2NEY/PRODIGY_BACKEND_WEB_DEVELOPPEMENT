from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

from app.api.base_responses.meta import Meta

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None
    meta: Optional[Meta] = None
