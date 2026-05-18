from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    EODHD_API_KEY: str | None = None
    DEBUG_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
