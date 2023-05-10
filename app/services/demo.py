from app.mappers.demo import DemoMapper


class DemoService(object):

    @staticmethod
    def add_demo(params):
        # return "Service - add_demo"
        return DemoMapper.add_demo(params)

    @staticmethod
    def delete_demo(id, params):
        # return "Service - delete_demo"
        return DemoMapper.delete_demo(id, params)

    @staticmethod
    def update_demo(params):
        # return "Service - update_demo"
        return DemoMapper.update_demo(params)

    @staticmethod
    def get_demo(id, params):
        # return "Service - get_demo"
        return DemoMapper.get_demo(id, params)

    @staticmethod
    def get_all_demo():
        # return "Service - get_all_demo"
        return DemoMapper.get_all_demo()
