from functools import lru_cache
from typing import List, Tuple, Type

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class Thresholds(BaseModel):
    MAX_SPEED_KMH: float
    MAX_ALTITUDE_M: float


class Settings(BaseSettings):
    SERVER_NAME: str
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    DEBUG: bool = False
    API_VERSION: str = "v1"
    SECRET_KEY: str

    DB_ASYNC_URI: str
    THRESHOLDS: Thresholds

    INTERVAL_SECONDS: int = 15

    model_config = SettingsConfigDict(json_file="settings.json", extra="ignore")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (JsonConfigSettingsSource(settings_cls),)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
