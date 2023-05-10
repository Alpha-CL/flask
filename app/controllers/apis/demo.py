from flask import request
from app.controllers.apis import apis_bp as app
from app.controllers.utils.rest_response import RestResponse, rest_full
from app.extensions import db_redis
from app.services.demo import DemoService

url_prefix = '/demo'


class DemoController(object):

    @staticmethod
    @app.route(f'{url_prefix}', methods=['POST'])
    def add_demo():
        params = request.form.to_dict()
        res = DemoService.add_demo(params)
        # return "Controller - add_demo"
        return RestResponse.success(res)

    @staticmethod
    @app.route(f'{url_prefix}/<int:id>', methods=['DELETE'])
    def delete_demo(id):
        params = request.args
        res = DemoService.delete_demo(id, params)
        # return "Controller - delete_demo"
        return RestResponse.success(res)

    @staticmethod
    @app.route(f'{url_prefix}', methods=['PUT'])
    def update_demo():
        params = request.form.to_dict()
        res = DemoService.update_demo(params)
        # return "Controller - update_demo"
        return RestResponse.success(res)

    @staticmethod
    @app.route(f'{url_prefix}/<int:id>', methods=['GET'])
    def get_demo(id):
        params = request.args
        data = DemoService.get_demo(id, params)
        # return "Controller - get_demo"
        return RestResponse.success(data)

    @staticmethod
    @app.route(f'{url_prefix}', methods=['GET'])
    @rest_full
    def get_all_demo():
        params = request.args
        data = DemoService.get_all_demo()
        # return "Controller - get_all_demo"
        return data
