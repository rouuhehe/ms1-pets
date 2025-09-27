from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        extra = "ignore"

settings = Settings()
