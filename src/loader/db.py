from sqlalchemy import Engine
from config import Settings
from sqlalchemy.ext.asyncio import create_async_engine


def create_engine(settings: Settings) -> Engine:
    return create_async_engine(settings.dsn)