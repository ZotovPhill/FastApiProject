import contextlib
from asyncio import current_task
from contextlib import contextmanager, AbstractContextManager
from typing import Callable

from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session
from sqlalchemy.orm import Session

from app.orm.base import Base


class AsyncDatabase:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = async_scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                class_=AsyncSession
            ),
            scopefunc=current_task
        )

    async def truncate_database(self) -> None:
        async with contextlib.closing(self._engine.connect()) as con:
            trans = await con.begin()
            for table in reversed(Base.sorted_tables):
                await con.execute(table.delete())
            await trans.commit()

    async def drop_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @contextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
