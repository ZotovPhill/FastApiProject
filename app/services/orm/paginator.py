from pydantic.main import BaseModel
from app.orm.schemas.base_schema import BasePaginator, LimitOffsetPaginator, PageSizePaginator


class Paginator:
    def __init__(self, model: BaseModel, paginator: BasePaginator) -> None:
        self.model = model
        self.paginator = paginator

    @classmethod
    def paginate(cls, query, model: BaseModel, paginator: BasePaginator):
        if isinstance(paginator, LimitOffsetPaginator):
            limit = paginator.limit
            offset = paginator.offset
        elif isinstance(paginator, PageSizePaginator):
            limit = paginator.page_size
            offset = paginator.page * paginator.page
        else:
            raise NotImplementedError("Paginator has not been implemented")

        total = query.count()
        items = query.limit(limit).offset(offset).all()

        return {
            "items": [model.from_orm(item) for item in items],
            "pagination": paginator.copy(
                update={
                    "total": total
                }
            )
        }
