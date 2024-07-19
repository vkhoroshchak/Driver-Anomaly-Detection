from functools import lru_cache
from typing import List, Tuple, Type

from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    SERVER_NAME: str
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    DEBUG: bool = False

    SECRET_KEY: str

    DB_ASYNC_URI: str

    model_config = SettingsConfigDict(json_file="settings.json")

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
