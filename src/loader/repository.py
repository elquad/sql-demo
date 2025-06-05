from sqlalchemy import literal_column

from .models import Url, Ip
from .db import get_session
from sqlalchemy.dialects.postgresql import insert


async def insert_urls(rows: list[dict]) -> int:
    stmt = (
        insert(Url)
        .values(rows)
        .on_conflict_do_nothing(index_elements=["url"])
        .returning(literal_column("1"))  # for counting the inserted rows
    )
    async with get_session() as s:
        result = await s.execute(stmt)
        count = sum(1 for _ in result.scalars())
        return count

async def insert_ips(rows: list[dict]) -> int:
    stmt = (
        insert(Ip)
        .values(rows)
        .on_conflict_do_nothing(index_elements=["address"])
        .returning(literal_column("1"))  # for counting the inserted rows
    )
    async with get_session() as s:
        result = await s.execute(stmt)
        count = sum(1 for _ in result.scalars())
        return count