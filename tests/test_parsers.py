import pytest
from loader.source import parse_alienvault_data, parse_abuse_data, parse_openphish_data
from loader.schema import Source

@pytest.mark.asyncio
async def test_parse_alienvault_data(good_alienvault_data):
    async def gen():
        for line in good_alienvault_data:
            yield line
    res = [row async for row in parse_alienvault_data(gen())]
    assert res == [{"address": "192.168.1.1", "source_id": int(Source.ALIENVAULT)},
                   {"address": "192.168.1.2", "source_id": int(Source.ALIENVAULT)}]

@pytest.mark.asyncio
async def test_parse_openphish_data(good_openphish_data):
    async def gen():
        for line in good_openphish_data:
            yield line
    res = [row async for row in parse_openphish_data(gen())]
    assert res == [{"url": "http://just-a-url.com/", "source_id": int(Source.OPENPHISH)},
                   {"url": "http://just-another-url.com/", "source_id": int(Source.OPENPHISH)}]

@pytest.mark.asyncio
async def test_parse_abuse_data(good_abuse_data):
    async def gen():
        for line in good_abuse_data:
            yield line
    res = [row async for row in parse_abuse_data(gen())]
    assert res == [{"url": "https://paste.ee/d/asdf", "source_id": int(Source.ABUSE)},
                   {"url": "http://127.0.0.1/400/bad.exe", "source_id": int(Source.ABUSE)}]