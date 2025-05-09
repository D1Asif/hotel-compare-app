from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = ".env"

settings = Settings() 