# File: app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://myuser:mypassword@localhost:5432/mydb")
    SECRET_KEY:str = os.getenv('SECRET_KEY', "supersecretkey")
    ALGORITHM:str = os.getenv('ALGORITHM', "HS256")

settings = Settings()
