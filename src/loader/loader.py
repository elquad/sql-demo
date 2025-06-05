import sys
import logging
from collections.abc import Callable
from typing import AsyncIterable, Any, Awaitable

from .config import Settings
from .repository import insert_urls, insert_ips
from .schema import Source
from .source import (parse_openphish_data, parse_alienvault_data, parse_abuse_data,
                     iterate_ioc_data, validate_url_rows, validate_ip_rows)
from .config import FEEDS
from .db import is_schema_present


BATCH = 5000
log = logging.getLogger(__name__)


async def load_data(
    feed: str,
    parser: Callable[[AsyncIterable[str]], AsyncIterable[dict[str, Any]]],
    validator: Callable[[AsyncIterable[dict[str, Any]]], AsyncIterable[dict[str, Any]]],
    inserter: Callable[[list[dict[str, Any]]], Awaitable[None]]
) -> None:
    raw_lines = iterate_ioc_data(feed)
    parsed = parser(raw_lines)
    validated = validator(parsed)

    batch: list[dict] = []
    inserted = 0
    async for row in validated:
        batch.append(row)
        if len(batch) == BATCH:
            inserted += await inserter(batch)   # uses ON CONFLICT DO NOTHING
            batch.clear()
    if batch:
        inserted += await inserter(batch)
    log.info(f"Inserted {inserted} rows from {str(feed)}")


async def run_pipeline() -> None:
    if not await is_schema_present():
        log.error("Database schema missing. Run `loader init-db` first.")
        sys.exit(1)

    for source, parser, validator, inserter in [
        (Source.OPENPHISH, parse_openphish_data, validate_url_rows, insert_urls),
        (Source.ALIENVAULT, parse_alienvault_data, validate_ip_rows, insert_ips),
        (Source.ABUSE, parse_abuse_data, validate_url_rows, insert_urls),
    ]:
        try:
            await load_data(FEEDS[source], parser, validator, inserter)
        except Exception as err:
            log.exception(f"Loading into feed {source.name} failed: {err}")