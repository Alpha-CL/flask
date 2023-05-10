from flask_restful import Resource, fields, marshal_with
from app.controllers.apis import apis_api as api
from app.controllers.utils.rest_response import RestResponse

rest_response = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.__all__
}


class TestController(Resource):

    # @marshal_with(rest_response)
    @staticmethod
    def get():
        return RestResponse.success('getTest')


api.add_resource(TestController, '/test', endpoint='test')
