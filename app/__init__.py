import os
from dotenv import load_dotenv
from flask import Flask
from app import controllers, extensions
from config import Config, configs

FLASK_ROOT_DIR = os.path.abspath(os.path.dirname('..'))
os.environ['FLASK_ROOT_DIR'] = FLASK_ROOT_DIR

BASE_DIR = os.path.abspath(os.path.dirname(FLASK_ROOT_DIR))
load_dotenv(os.path.join(BASE_DIR, '.flaskenv'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


def create_app(config=Config):
    path = os.path.dirname(__file__)
    templates = os.path.abspath(os.path.join(path, os.pardir, 'templates'))
    static = os.path.abspath(os.path.join(path, os.pardir, 'static'))

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=templates,
        static_folder=static,
    )

    # Get the current environment variable
    env = os.getenv("FLASK_ENV") or "production"

    print(f'[ENVIRONMENT_FLASK_ENV]: {os.getenv("FLASK_ENV")}')
    print(f'[CONFIG_FLASK_ENV]: {app.config.get("ENV")}')

    # Set configuration information based on environment variables
    env_config = configs.get(env)
    app.config.from_object(env_config)

    print(f'[CONFIG]: {config}')
    print(f'[ENV_CONFIG]: {env_config}')

    extensions.init_app(app)
    controllers.init_app(app)

    # print(f'[url_map]: {app.url_map}')  # print all route

    return app


from app.models import *
