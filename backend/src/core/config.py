from pydantic_settings import BaseSettings
from typing import Literal

import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    db_url: str = os.getenv("POSTGRES_URL")  # Вот так добавить

    environment: Literal["development", "staging", "production"] = "development"


settings = Settings()