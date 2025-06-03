# fetch → parse → repo pipeline
import asyncio
from .config import Settings
from .db import get_session

async def run_pipeline(settings: Settings) -> None:
    async with get_session() as s:
        ...