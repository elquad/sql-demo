import pytest
from loader.source import validate_url_rows, validate_ip_rows
from loader.schema import Source

@pytest.mark.asyncio
async def test_good_url_passes(good_url_row):
    async def gen():
        yield good_url_row
    clean = [row async for row in validate_url_rows(gen())]
    assert clean == [{"url": "https://example.com/", "source_id": int(Source.OPENPHISH)}]

@pytest.mark.asyncio
async def test_bad_url_rejected(bad_url_row):
    async def gen():
        yield bad_url_row
    clean = [row async for row in validate_url_rows(gen())]
    assert clean == []

@pytest.mark.asyncio
async def test_good_ip_passes(good_ip_row):
    async def gen():
        yield good_ip_row
    clean = [row async for row in validate_ip_rows(gen())]
    assert clean == [{"address": "192.168.3.4", "source_id": int(Source.ALIENVAULT)}]

@pytest.mark.asyncio
async def test_bad_ip_rejected(bad_ip_row):
    async def gen():
        yield bad_ip_row
    clean = [row async for row in validate_ip_rows(gen())]
    assert clean == []