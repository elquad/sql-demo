from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from .models import Base

async def bootstrap(dsn: str) -> None:
    engine = create_async_engine(
        dsn,
        pool_size=2,
        isolation_level="AUTOCOMMIT",  # needed for CREATE EXTENSION
    )
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            text(
                """
                INSERT INTO source (id, name) VALUES
                    (1, 'Abuse'),
                    (2, 'AlienVault'),
                    (3, 'OpenPhish')
                ON CONFLICT DO NOTHING
                """
            )
        )
    await engine.dispose()