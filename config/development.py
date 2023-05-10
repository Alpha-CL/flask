import os
from config.base import Config


# development environment
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"{os.getenv('SQLALCHEMY_DATABASE_URI')}/dev"

    # dialect+driver://username:password@host:port/database
    # 特殊字符需要转译( @ == %40，% == %25 )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库修改，一般不开启, 会影响性能
    SQLALCHEMY_POOL = 20
    SQLALCHEMY_POOL_RECYCLE = 3000

    # flask redis
    REDIS_URL = os.getenv('REDIS_URL') or 'redis://'

    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    REDIS_DB = os.getenv('REDIS_DB', '0')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    DECODE_RESPONSES = os.getenv('REDIS_PASSWORD')

    # redis
    REDIS_CONFIG = {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': REDIS_DB,
        'password': REDIS_PASSWORD,
        'decode_responses': DECODE_RESPONSES
    }

    # flask apscheduler
    # SCHEDULER_TIMEZONE                # 配置时区
    # SCHEDULER_API_PREFIX              # 配置API路由前缀
    # SCHEDULER_ENDPOINT_PREFIX         # 配置API路由后缀
    # SCHEDULER_ALLOWED_HOSTS           # 配置访问白名单
    # SCHEDULER_AUTH                    # 配置认证中心
    SCHEDULER_JOBSTORES = {
        # 'default': SQLAlchemyJobStore(url='sqlite://')
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }
    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(app):
        pass
