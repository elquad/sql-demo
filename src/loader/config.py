from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    dsn: str = "postgresql://postgres:postgres@localhost/sql-demo"
    batch_size: int = 5000
    pool_size: int = 10

    model_config = SettingsConfigDict(
        env_prefix="LOADER_",
        env_file=".env",
    )


def load_settings(args) -> Settings:
    """Merge CLI overrides into Pydantic Settings."""
    cli_overrides = {k: v for k, v in vars(args).items() if v is not None}
    return Settings(**cli_overrides)