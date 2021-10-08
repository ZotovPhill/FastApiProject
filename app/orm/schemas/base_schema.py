import json
import math
import enum
from typing import Optional

from pydantic import BaseModel, validator
from pydantic.fields import Field


class BaseIdModel(BaseModel):
    id: Optional[int]

    class Config:
        orm_mode = True


class BaseFilter(BaseModel):
    id: Optional[int]

    class Config:
        extra = "forbid"


class OrderEnum(str, enum.Enum):
    ASC = "ASC"
    DESC = "DESC"


class BaseSort(BaseModel):
    id: Optional[OrderEnum]

    class Config:
        extra = "forbid"


class BasePaginator(BaseModel):
    total: int = 0
    has_previous: bool = False
    has_next: bool = False

    class Config:
        extra = "forbid"


class LimitOffsetPaginator(BasePaginator):
    limit: int = Field(default=50, ge=0)
    offset: int = Field(default=0, ge=0)

    @validator("has_previous")
    def has_previous_result(cls, value):
        return cls.offset != 0

    @validator("has_next")
    def has_next_result(cls, value):
        return cls.limit + cls.offset < cls.total


class PageSizePaginator(BasePaginator):
    page_size: int = Field(default=50, ge=0)
    page: int = Field(default=1, ge=1)
    pages: int = Field(default=0, ge=0)

    @validator("pages")
    def total_pages(cls, value):
        assert int(value) >= 0, "Value must be positive integer"
        return int(math.ceil(cls.total / float(cls.page_size)))

    @validator("has_previous")
    def has_previous_result(cls, value):
        return cls.page > 1

    @validator("has_next")
    def has_next_result(cls, value):
        return cls.page + 1 <= cls.pages


class QueryParam(BaseModel):
    filter: Optional[BaseFilter]
    sort: Optional[BaseSort]
    paginator: Optional[BasePaginator]

    @classmethod
    async def as_obj(
            cls,
            filter: Optional[str],
            sort: Optional[str],
            paginator: Optional[str]
    ):
        return cls(
            filter=json.loads(filter),
            sort=json.loads(sort),
            paginator=json.loads(paginator)
        )
