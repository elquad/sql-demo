from enum import IntEnum
from pydantic import BaseModel, IPvAnyAddress, HttpUrl


class Source(IntEnum):
    ABUSE = 1
    ALIENVAULT = 2
    OPENPHISH = 3


class UrlRow(BaseModel):
    url: HttpUrl
    source_id: Source


class IpAddrRow(BaseModel):
    address: IPvAnyAddress
    source_id: Source