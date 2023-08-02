from flask import Blueprint, jsonify
from flask_restful import Api

from werkzeug.utils import import_string
from app.controllers.utils.error_handler import init_error_handlers

# create blueprint
controllers_url_prefix = '/controllers'
controllers_bp = Blueprint('controllers', __name__, url_prefix=controllers_url_prefix)
controllers_api = Api(controllers_bp)


def init_app(app):
    # mount blueprint node
    app.register_blueprint(controllers_bp)

    blueprints = [
        "app.controllers.apis",
        "app.controllers.auth",
    ]
    for blueprint in blueprints:
        # import blueprint package
        import_string(blueprint).init_app(app)

    init_error_handlers(app)


# import module
from . import apis, auth
