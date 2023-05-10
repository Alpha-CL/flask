from config.base import Config
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.testing import TestingConfig

configs = {
    "default": Config,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
