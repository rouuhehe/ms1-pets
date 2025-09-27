from .default import Settings as DefaultSettings


class ProductionSettings(DefaultSettings):
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
