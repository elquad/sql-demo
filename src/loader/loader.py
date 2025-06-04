import sys

from .config import Settings
from .repository import insert_urls, insert_ips
from .schema import Source
from .source import (parse_openphish_data, parse_alienvault_data, parse_abuse_data,
                     iterate_ioc_data, validate_url_rows, validate_ip_rows)
from .config import FEEDS
from .db import is_schema_present


BATCH = 5000


async def load_data(feed, parser, validator, inserter):
    raw_lines = iterate_ioc_data(feed)
    parsed = parser(raw_lines)
    validated = validator(parsed)

    batch: list[dict] = []
    async for row in validated:
        batch.append(row)
        if len(batch) == BATCH:
            await inserter(batch)   # uses ON CONFLICT DO NOTHING
            batch.clear()
    if batch:
        await inserter(batch)


async def run_pipeline(settings: Settings) -> None:
    if not await is_schema_present():
        print("Schema missing. Run `loader init-db` first.", file=sys.stderr)
        sys.exit(1)


    await load_data(FEEDS[Source.OPENPHISH], parse_openphish_data, validate_url_rows, insert_urls)
    await load_data(FEEDS[Source.ALIENVAULT], parse_alienvault_data, validate_ip_rows, insert_ips)
    await load_data(FEEDS[Source.ABUSE], parse_abuse_data, validate_url_rows, insert_urls)
    print("Loaded.")