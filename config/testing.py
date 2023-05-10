import os
from config.base import Config


# testing environment
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')

    @staticmethod
    def init_app(app):
        pass
