from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from .schema import Source


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    dsn: str
    batch_size: int = 5000
    pool_size: int = 10

    model_config = SettingsConfigDict(
        env_prefix="LOADER_",
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


FEEDS: dict[Source, str] = {
    Source.ABUSE: "https://urlhaus.abuse.ch/downloads/csv_recent/",
    Source.ALIENVAULT: "http://reputation.alienvault.com/reputation.data",
    Source.OPENPHISH: "https://openphish.com/feed.txt",
}


def load_settings(args) -> Settings:
    """Merge CLI overrides into Pydantic Settings."""
    cli_overrides = {k: v for k, v in vars(args).items() if v is not None}
    return Settings(**cli_overrides)