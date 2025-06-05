import csv
from collections.abc import AsyncIterator
import aiohttp
from pydantic_core import ValidationError
import logging

from .schema import Source, UrlRow, IpAddrRow


log = logging.getLogger(__name__)


async def iterate_ioc_data(
    src: str,
    *,
    encoding: str = "utf-8",
    chunk_size: int = 4096
) -> AsyncIterator[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(src) as response:
            response.raise_for_status()

            buffer = ""
            async for chunk in response.content.iter_chunked(chunk_size):
                if not chunk:
                    continue

                buffer += chunk.decode(encoding)
                *lines, buffer = buffer.splitlines(keepends=False)  # buffer will contain potentially unfinished line

                for line in lines:
                    if line:
                        yield line

            # flush tail if the file didn't end with '\n'
            if buffer:
                yield buffer


async def validate_url_rows(raw_lines: AsyncIterator[dict]) -> AsyncIterator[dict]:
    async for line in raw_lines:
        try:
            row = UrlRow(**line)
        except ValidationError as err:
            log.warning(f"Skipped invalid row: {line}.")
            continue
        yield {"url": str(row.url), "source_id": int(row.source_id)}


async def validate_ip_rows(raw_lines: AsyncIterator[dict]) -> AsyncIterator[dict]:
    async for line in raw_lines:
        try:
            row = IpAddrRow(**line)
        except ValidationError as err:
            log.warning(f"Skipped invalid row: {line}.")
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