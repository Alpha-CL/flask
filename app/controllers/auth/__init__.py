from flask import Blueprint
from flask_restful import Api

auth_url_prefix = '/auth'
auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp)


def init_app(app):
    app.register_blueprint(auth_bp, url_prefix=auth_url_prefix)
