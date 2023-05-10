from enum import Enum


class ResultCode(Enum):
    """
    success: 200
    """
    SUCCESS = (0, 'request is successful')
    """
    params fail
    """
    FAIL = (-1, 'request is failed')
    """
    user fail
    """
    TOKEN_INVALID = (40001, 'token is null or invalid')
    ACCESS_DENIED = (40003, 'access denied')
    FAIL4DELETE = (50001, 'delete failed')
    FAIL4UPDATE = (50002, 'update failed')

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def get_code(self):
        return self.code

    def get_msg(self):
        return self.msg
