from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Easy List"
    VERSION: int = 1
    ENV: Literal["dev", "prod"] = "dev"
    JWT_SECRET_KEY: str 

    DATABASE_URL: str = "sqlite:///./easylist.db"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = Field(default=5, gt=0)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0)
    DB_POOL_TIMEOUT: int = Field(default=30, gt=0)
    DB_POOL_RECYCLE: int = 1800
    DB_POOL_PRE_PING: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
