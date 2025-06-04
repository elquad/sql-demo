"""
Async-only database helpers backed by SQLAlchemy + psycopg3.
"""
from __future__ import annotations
from .config import Settings

from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


# Module-level singletons (populated by init_engine)
_engine: AsyncEngine | None = None
_SessionFactory: async_sessionmaker[AsyncSession] | None = None


async def init_engine(settings: Settings) -> None:
    global _engine, _SessionFactory
    _engine = create_async_engine(
        f"postgresql+psycopg://{settings.dsn.removeprefix('postgresql://')}",
        pool_size=settings.pool_size,
        pool_pre_ping=True,                       # drop & replace dead conns
    )

    _SessionFactory = async_sessionmaker(
        _engine,
        expire_on_commit=False,                   # don’t invalidate attributes
    )


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    if _SessionFactory is None:
        raise RuntimeError("init_engine() must be called before get_session().")

    async with _SessionFactory() as session:
        try:
            yield session
            await session.commit()
        except BaseException:
            await session.rollback()
            raise


async def dispose_engine() -> None:
    if _engine is not None:
        await _engine.dispose()