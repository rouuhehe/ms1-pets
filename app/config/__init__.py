import os
from .default import settings as default_settings
from .development import DevelopmentSettings
from .production import ProductionSettings
from .testing import TestingSettings

env = os.getenv("APP_ENV", "default")

if env == "development":
    settings = DevelopmentSettings()
elif env == "production":
    settings = ProductionSettings()
elif env == "testing":
    settings = TestingSettings()
else:
    settings = default_settings
