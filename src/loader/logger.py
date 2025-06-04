# loader/logging_utils.py
import json, logging, os, sys
from datetime import datetime
from typing import Mapping


class DevFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        msg = super().format(record)
        return f"{timestamp} | {record.levelname:<8} | {msg}"


def setup_logging() -> None:
    log_level = os.getenv("LOADER_LOG_LEVEL", "INFO").upper()

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(DevFormatter("%(message)s"))

    root = logging.getLogger()
    root.setLevel(log_level)
    root.handlers[:] = [handler]  # replace default handler noise
    # Quiet aiohttp and SQLAlchemy
    logging.getLogger("aiohttp").setLevel("WARNING")
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if log_level == "DEBUG" else "WARNING"
    )
