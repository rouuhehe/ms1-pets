from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DEBUG: bool = False
    TESTING: bool = False
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    ITEMS_PER_PAGE: int = 20
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")
    APP_ENV: str = "default"
    '''
    S3_BASE_URL: str = os.getenv("S3_BASE_URL")
    S3_BUCKET: str = os.getenv("S3_BUCKET")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN: str = os.getenv("AWS_SESSION_TOKEN")
    AWS_DEFAULT_REGION: str = os.getenv("AWS_DEFAULT_REGION")
    '''
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
