from .models import Url, Ip
from .db import get_session
from sqlalchemy.dialects.postgresql import insert


async def insert_urls(rows: list[dict]) -> None:
    stmt = (
        insert(Url)
        .values(rows)
        .on_conflict_do_nothing(index_elements=["url"])
    )
    async with get_session() as s:
        await s.execute(stmt)


async def insert_ips(rows: list[dict]) -> None:
    stmt = (
        insert(Ip)
        .values(rows)
        .on_conflict_do_nothing(index_elements=["address"])
    )
    async with get_session() as s:
        await s.execute(stmt)