from flask import jsonify
from sqlalchemy.orm import DeclarativeMeta

from app.controllers.utils.result_code import ResultCode


class RestResponse(object):
    data = None
    code = None
    msg = None

    success_code = ResultCode.SUCCESS.value[0] or 0
    success_msg = ResultCode.SUCCESS.value[1] or 'success'

    fail_code = ResultCode.FAIL.value[0] or -1
    fail_msg = ResultCode.FAIL.value[1] or 'fail'

    def __init__(self, data, code, msg):
        self.data = data
        self.code = code
        self.msg = msg

    @classmethod
    def success(cls, data=None, code=success_code, msg=success_msg):
        result_code, result_msg = cls.get_result_enum(ResultCode, 'success')
        rest_response = cls(
            data,
            code if code != cls.success_code else result_code,
            msg if msg != cls.success_msg else result_msg
        )
        return rest_response.to_dict()

    @classmethod
    def error(cls, data=None, code=fail_code, msg=fail_msg, name='fail'):
        result_code, result_msg = cls.get_result_enum(ResultCode, name)
        rest_response = cls(
            data,
            code if code != cls.fail_code else result_code,
            msg if msg != cls.fail_msg else result_msg
        )
        return rest_response.to_dict()

    @classmethod
    def get_result_enum(cls, result_code_enum, name):
        if hasattr(result_code_enum, name.upper()):
            return result_code_enum[name.upper()].value
        else:
            return 0, f'{result_code_enum.__name__} not has {name}'

    def to_dict(self):
        response_data = {
            "code": self.code,
            "msg": self.msg,
            "data": self.serialize(self.data)
        }
        try:
            response_data['data'] = self.serialize(self.data)
            return jsonify(response_data)
        except SerializationError as e:
            response_data['code'] = e.code
            response_data['msg'] = e.msg
            return jsonify(response_data)

    @staticmethod
    def serialize(obj):
        if obj is None:
            return None
        try:
            # 如果对象本身就是可以序列化为JSON的类型，则直接返回
            if isinstance(obj, (str, int, float, bool, list, tuple, dict)):
                return obj
            # 如果对象是ORM对象，则将其转换为字典并返回
            elif isinstance(obj.__class__, DeclarativeMeta):
                return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
            # 如果对象实现了__dict__方法，则将其转换为字典并返回
            elif hasattr(obj, '__dict__'):
                return obj.__dict__
            # 如果对象是其他类型，则抛出异常
            else:
                raise SerializationError(code=500, msg='cannot serialize object')
        except Exception as e:
            raise SerializationError(code=500, msg=str(e))


class SerializationError(Exception):
    """
    自定义的异常类，用于处理序列化错误
    """

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


def rest_full(callback):
    return rest_full_success(callback)


def rest_full_success(callback):
    def func(*args, **kwargs):
        res = callback(*args, **kwargs)
        return RestResponse.success(res)

    return func


def rest_full_error(callback):
    def func(*args, **kwargs):
        res = callback(*args, **kwargs)
        return RestResponse.error(res)

    return func
