from flask import Blueprint
from flask_restful import Api

from app.utils.module import import_all

apis_url_prefix = '/api'
apis_bp = Blueprint('apis', __name__)
apis_api = Api(apis_bp)


def init_app(app):
    app.register_blueprint(apis_bp, url_prefix=apis_url_prefix)


import_all(__file__, __name__, __path__)
