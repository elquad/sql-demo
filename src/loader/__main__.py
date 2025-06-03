from .cli import get_args
from .config import load_settings
from .db import init_engine
from .loader import run_pipeline    # the business logic


async def main() -> None:
    cmdline_args = get_args()
    settings = load_settings(cmdline_args)
    await init_engine(settings)
    await run_pipeline(settings)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())