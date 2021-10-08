import contextlib
from contextlib import contextmanager, AbstractContextManager
from typing import Callable

from pydantic.main import BaseModel
from sqlalchemy import create_engine, orm
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.exceptions.exceptions import NotFoundException
from app.orm.base import Base
from app.orm.schemas.base_schema import BaseFilter, BaseIdModel, BasePaginator, BaseSort
from app.services.orm.paginator import Paginator


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def truncate_database(self) -> None:
        with contextlib.closing(self._engine.connect()) as con:
            trans = con.begin()
            for table in reversed(Base.sorted_tables):
                con.execute(table.delete())
            trans.commit()

    def drop_database(self) -> None:
        Base.metadata.drop_all(self._engine)

    def create_database(self) -> None:
        # from app.orm.models.users.employee import Employee
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class Meta(type):
    def __new__(cls, name, bases, attrs):
        newattrs = {}
        for attrname, attrvalue in attrs.items():
            if attrname == '__model__':
                newattrs[attrname.removesuffix('__').removeprefix('__')] = attrvalue
            else:
                newattrs[attrname] = attrvalue

        return super().__new__(cls, name, bases, newattrs)


class BaseRepository(metaclass=Meta):
    model = None

    def __init__(
            self,
            session_factory: Callable[..., AbstractContextManager[Session]],
            serializer: BaseModel = BaseIdModel,
    ) -> None:
        self.session_factory = session_factory
        self.serializer = serializer

    def find_all(self):
        with self.session_factory() as session:
            return session.query(self.model).all()

    def universal_filter_sort(self, filters: BaseFilter, sorts: BaseSort, paginator: BasePaginator):
        with self.session_factory() as session:
            query = session.query(self.model).filter_by(**filters.dict(exclude_none=True))
            return Paginator.paginate(query, self.serializer, paginator)

    def find(self, id: int):
        with self.session_factory() as session:
            result = session.query(self.model).get(id)
            if not result:
                raise NotFoundException(id, self.model.__name__)
            return result

    def count(self):
        with self.session_factory() as session:
            return session.query(func.count(self.model.id)).scalar()

    def create(self, model: BaseIdModel):
        with self.session_factory() as session:
            entity = self.model(**model.dict(exclude={"id"}))
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def update(self, model: BaseIdModel):
        with self.session_factory() as session:
            session.query(self.model) \
                .filter_by(id=model.id) \
                .update(
                model.dict(exclude={"id"}, exclude_none=True),
            )
            session.commit()

            return self.find(model.id)

    def delete(self, id: int):
        with self.session_factory() as session:
            entity = session.query(self.model).filter_by(id=id).first()
            session.delete(entity)
            session.commit()

    def bulk_save(self, models: list[BaseIdModel]):
        objects = [self.model(**model.dict(exclude={"id"})) for model in models]
        with self.session_factory() as session:
            session.bulk_save_objects(objects)
            session.commit()
