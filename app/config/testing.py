from .default import Settings as DefaultSettings
import os


class TestingSettings(DefaultSettings):
    TESTING: bool = True
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

    DATABASE_URL: str = "sqlite:///:memory:"
