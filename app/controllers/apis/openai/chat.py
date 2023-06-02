from flask import request
from app.controllers.apis.openai import openai_bp as app

# from app.services.chat import ChatService

url_prefix = '/chat'


class ChatController(object):

    @staticmethod
    @app.route(f'{url_prefix}', methods=['POST'])
    def add_chat():
        params = request.form.to_dict()
        # res = ChatService.add_chat(params)
        return "Controller - add_chat"
        # return RestResponse.success(res)

    @staticmethod
    @app.route(f'{url_prefix}/<int:id>', methods=['DELETE'])
    def delete_chat(id):
        params = request.args
        # res = ChatService.delete_chat(id, params)
        return "Controller - delete_chat"
        # return RestResponse.success(res)

    @staticmethod
    @app.route(f'{url_prefix}', methods=['PUT'])
    def update_chat():
        params = request.form.to_dict()
        # res = ChatService.update_chat(params)
        return "Controller - update_chat"
        # return RestResponse.success(res)

    @staticmethod
    @app.route(f'{url_prefix}/<int:id>', methods=['GET'])
    def get_chat(id):
        params = request.args
        # data = ChatService.get_chat(id, params)
        return "Controller - get_chat"
        # return RestResponse.success(data)

    @staticmethod
    @app.route(f'{url_prefix}', methods=['GET'])
    def get_all_chat():
        params = request.args
        # data = ChatService.get_all_chat()
        return "Controller - get_all_chat"
        # return RestResponse.success(data)
