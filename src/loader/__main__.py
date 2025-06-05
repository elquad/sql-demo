import sys

from pydantic import ValidationError
import logging

from .init_db import bootstrap
from .cli import get_args
from .config import load_settings
from .db import init_engine
from .loader import run_pipeline
from .logger import setup_logging

async def main() -> None:
    setup_logging()
    log = logging.getLogger(__name__)
    cmdline_args = get_args()
    try:
        settings = load_settings(cmdline_args)
    except ValidationError:
        log.error("Configuration error: DSN not set. "
            "Set LOADER_DSN or use --dsn in format 'postgresql://[user[:password]@][host][:port][/dbname]'")
        sys.exit(1)
    settings.dsn = f"postgresql+psycopg://{settings.dsn.removeprefix('postgresql://')}"

    if cmdline_args.cmd == "init-db":
        await bootstrap(settings.dsn)
        log.info("init-db ended successfully")
        sys.exit(0)

    await init_engine(settings)
    await run_pipeline()
    log.info("Ended successfully.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())