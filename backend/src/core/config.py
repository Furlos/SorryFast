from pydantic_settings import BaseSettings
from typing import Literal

import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    db_url = os.getenv("POSTGRES_URL")

    environment: Literal["development", "staging", "production"] = "development"


settings = Settings()
