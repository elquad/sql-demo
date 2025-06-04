import sys

from pydantic import ValidationError
from .cli import get_args
from .config import load_settings
from .db import init_engine
from .loader import run_pipeline


async def main() -> None:
    cmdline_args = get_args()
    try:
        settings = load_settings(cmdline_args)
    except ValidationError:
        print("Configuration error: DSN not set.\n"
            "Set LOADER_DSN or use --dsn in format 'postgresql://[user[:password]@][host][:port][/dbname]'")
        sys.exit(1)
    await init_engine(settings)
    await run_pipeline(settings)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())