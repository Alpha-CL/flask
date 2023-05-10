import os
import sys

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.parse
else:
    import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


# base configuration
class Config(object):
    APP_NAME = os.getenv('APP_NAME') or 'flask-webapp'
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('secret_key env var not set! should not see in production')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_ECHO = True  # 是否显示底层执行的SQL语句

    @staticmethod
    def init_app(app):
        print('THIS APP IS IN DEBUG MODE. \
                        YOU SHOULD NOT SEE THIS IN PRODUCTION.')
