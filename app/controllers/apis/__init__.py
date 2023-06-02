from flask import Blueprint
from flask_restful import Api

from werkzeug.utils import import_string

# create blueprint
apis_url_prefix = '/apis'
apis_bp = Blueprint('apis', __name__, url_prefix=apis_url_prefix)
apis_api = Api(apis_bp)


def init_app(parent):
    # mount blueprint node
    parent.register_blueprint(apis_bp)

    blueprints = [
        "app.controllers.apis.openai",
    ]
    for blueprint in blueprints:
        # import blueprint package
        import_string(blueprint).init_app(parent)


# import module
from . import openai
