from functools import lru_cache
from typing import Literal, NamedTuple

from pydantic_settings import BaseSettings, SettingsConfigDict

SameSitePolicy = Literal["lax", "strict", "none"]


class CookieConfig(NamedTuple):
    samesite: SameSitePolicy
    secure: bool


class Settings(BaseSettings):
    """Application settings, populated from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MARIAMBIKA_",
        extra="ignore",
    )

    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_ENVIRONMENT: str

    SERVER_NAME: str
    SERVER_PATH: str
    SERVER_HOST: str
    SERVER_PORT: int
    SERVER_RELOAD: bool
    SERVER_BASE_API: str

    DATABASE_LOCAL_NAME: str
    DATABASE_LOCAL_URL: str
    DATABASE_PRODUCTION_NAME: str
    DATABASE_PRODUCTION_URL: str
    DATABASE_AUTO_COMMIT: bool
    DATABASE_AUTO_FLUSH: bool
    DATABASE_ECHO_LOGS: bool

    REFRESH_TOKEN_SECRET_KEY: bytes
    REFRESH_TOKEN_EXPIRES_AT: int
    ACCESS_TOKEN_SECRET_KEY: str
    JWT_TOKEN_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_IN: int

    LOCAL_COOKIE_SECURE: bool
    LOCAL_COOKIE_SAMESITE: SameSitePolicy
    PRODUCTION_COOKIE_SECURE: bool
    PRODUCTION_COOKIE_SAMESITE: SameSitePolicy

    @property
    def switch_db_using_env(self) -> str:
        if self.APP_ENVIRONMENT == "dev":
            return self.DATABASE_LOCAL_URL

        elif self.APP_ENVIRONMENT == "prod":
            return self.DATABASE_PRODUCTION_URL

        raise ValueError(
            f"Invalid APP_ENVIRONMENT: {self.APP_ENVIRONMENT}. Expected 'dev' or 'prod'."
        )

    @property
    def switch_cookies_set_based_on_env(self) -> CookieConfig:
        if self.APP_ENVIRONMENT == "dev":
            return CookieConfig(
                samesite=self.LOCAL_COOKIE_SAMESITE, secure=self.LOCAL_COOKIE_SECURE
            )
        return CookieConfig(
            samesite=self.PRODUCTION_COOKIE_SAMESITE,
            secure=self.PRODUCTION_COOKIE_SECURE,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


APP_SETTINGS = get_settings()
