import contextlib
from contextlib import contextmanager, AbstractContextManager
from typing import Callable

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session

from app.orm.base import Base


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
