from typing import Optional

from app.orm.schemas.base_schema import (
    BaseFilter,
    BaseSort,
    LimitOffsetPaginator,
    QueryParam,
)


class EmployeeFilter(BaseFilter):
    email: Optional[str]


class EmployeeSort(BaseSort):
    email: Optional[str]


class EmployeeQueryParam(QueryParam):
    filter: Optional[EmployeeFilter]
    sort: Optional[EmployeeSort]
    paginator: Optional[LimitOffsetPaginator]
