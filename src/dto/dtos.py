from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class PaginatedEntityList(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    pages: int
    page_size: int