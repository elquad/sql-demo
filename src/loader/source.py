import csv
from collections.abc import AsyncIterator
import aiohttp
from aiocsv import AsyncDictReader
from pydantic_core import ValidationError

from .schema import Source, UrlRow, IpAddrRow


async def iterate_ioc_data(src: str, *, encoding: str = "utf-8") -> AsyncIterator[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(src) as response:
            response.raise_for_status()
            async for chunk in response.content:
                if chunk:
                    yield chunk.decode(encoding).rstrip("\n")


async def validate_url_rows(raw_lines: AsyncIterator[dict]) -> AsyncIterator[dict]:
    async for line in raw_lines:
        try:
            row = UrlRow(**line)
        except ValidationError as err:
            #  log skip
            continue
        yield {"url": str(row.url), "source_id": int(row.source_id)}


async def validate_ip_rows(raw_lines: AsyncIterator[dict]) -> AsyncIterator[dict]:
    async for line in raw_lines:
        try:
            row = IpAddrRow(**line)
        except ValidationError as err:
            #  log skip
            continue
        yield {"address": str(row.address), "source_id": int(row.source_id)}


async def parse_abuse_data(lines: AsyncIterator[str]) -> AsyncIterator[dict]:
    async for line in lines:
        if line.startswith("#"):
            continue

        row = next(csv.reader([line]))
        entry = dict(
            zip(["id", "dateadded", "url", "url_status", "last_online", "threat",
                 "tags", "urlhaus_link", "reporter"], row)
        )
        yield {"url": entry["url"], "source_id": int(Source.ABUSE)}


async def parse_alienvault_data(lines: AsyncIterator[str]) -> AsyncIterator[dict]:
    async for line in lines:
        ip = line.split("#", 1)[0].strip()
        if ip:
            yield {"address": ip, "source_id": int(Source.ALIENVAULT)}


async def parse_openphish_data(lines: AsyncIterator[str]) -> AsyncIterator[dict]:
    async for line in lines:
        url = line.strip()
        if url:
            yield {"url": url, "source_id": int(Source.OPENPHISH)}