from typing import Annotated, Any, Literal, List
import json
from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config= SettingsConfigDict(
        env_file= "Backend_py/.env",
        env_ignore_empty= True,
        extra= "ignore"
    )

    PROJECT_NAME: str = "AI_SAAS_TEMPLATE"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "Perceptron"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*8
    ENVIRONMENT: Literal["development", "production"]= "development"
    FRONTEND_HOST: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    @property
    def all_cors_origin(self)->list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
        self.FRONTEND_HOST
    ]
    # DB connection settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_URL: str
    

    
settings = Settings()
