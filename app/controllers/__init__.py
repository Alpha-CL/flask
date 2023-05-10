import sys

from flask import Blueprint
from flask_restful import Api
from app.utils.module import import_all

controllers_url_prefix = ''
controllers_bp = Blueprint('controllers', __name__, url_prefix='')
controllers_api = Api(controllers_bp)


def init_app(app):
    app.register_blueprint(controllers_bp, url_prefix=controllers_url_prefix)
    import_all(__file__, __name__, __path__, app=app)
