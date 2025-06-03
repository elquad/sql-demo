from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    dsn: PostgresDsn            # postgresql+psycopg2://user:password@host:port/dbname
    async_mode: bool = False
    batch_size: int = 5000

    model_config = SettingsConfigDict(
        env_prefix="LOADER_",
        env_file=".env",
    )


settings = Settings()