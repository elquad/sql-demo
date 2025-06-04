import csv
from io import StringIO
from typing import Iterator

import requests

from .schema import Source


def iterate_ioc_data(source: str, encoding='utf-8') -> Iterator[str]:
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source, stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                yield line.decode(encoding)
    else:
        with open(source, 'r', encoding=encoding) as f:
            yield from f


def parse_abuse_data(content: StringIO) -> list[dict[str,str|int]]:
    filtered_lines = (line for line in content if not line.startswith("#"))
    reader = csv.DictReader(filtered_lines, fieldnames=[
        "id", "dateadded", "url", "url_status", "last_online", "threat", "tags", "urlhaus_link", "reporter"
    ])
    rows = [{'url': entry.get('url'), 'source': int(Source.ABUSE)} for entry in reader]
    return rows


def parse_alienvault_data(content):
    return [{'ip': line.split("#", 1)[0], 'source': int(Source.ALIENVAULT)} for line in content]


def parse_openphish_data(content):
    return [{'url': line.strip(), 'source': int(Source.OPENPHISH)} for line in content]