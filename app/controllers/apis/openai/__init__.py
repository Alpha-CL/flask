from flask import Blueprint
from flask_restful import Api

from werkzeug.utils import import_string

# create blueprint
openai_url_prefix = '/api/openai'
openai_bp = Blueprint('openai', __name__, url_prefix=openai_url_prefix)
openai_api = Api(openai_bp)


def init_app(parent):
    # mount blueprint node
    parent.register_blueprint(openai_bp)

    # blueprints = [
    #     "app.controllers.apis.openai",
    # ]
    # for blueprint in blueprints:
    #     # import blueprint package
    #     import_string(blueprint).init_app(parent)


# import module
from . import chat
