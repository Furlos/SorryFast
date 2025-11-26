from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    pg_host: str
    pg_port: int = 5432
    pg_user: str
    pg_password: str
    pg_database: str

    enviroment: Literal["development", "staging", "production"] = "development"


    class Config:
        env_file = "../../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
