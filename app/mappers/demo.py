from app.extensions import db
from app.models.demo import DemoModel


class DemoMapper(object):

    @staticmethod
    def add_demo(params):
        return "Mapper - add_demo"

    @staticmethod
    def delete_demo(id, params):
        return "Mapper - delete_demo"

    @staticmethod
    def update_demo(params):
        return "Mapper - update_demo"

    @staticmethod
    def get_demo(id, params):
        return "Mapper - get_demo"

    @staticmethod
    def get_all_demo():
        return "Mapper - get_all_demo"
