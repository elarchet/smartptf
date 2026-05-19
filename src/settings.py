from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PathConfig(BaseModel):
    index_compo: Path = Path("./data/index_compo/")
    index_historical: Path = Path("./data/index_historical/")

class Settings(BaseSettings):
    EODHD_API_KEY: str | None = None
    DEBUG_MODE: bool = False
    
    paths: PathConfig = Field(default_factory=PathConfig)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
