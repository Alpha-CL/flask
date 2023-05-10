import os
from config.base import Config


# production environment
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_PROD')

    @staticmethod
    def init_app(app):
        pass
