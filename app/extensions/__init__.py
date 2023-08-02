import os
import rq
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from flask_apscheduler import APScheduler
from app.utils.db_sqlalchemy import DBMysqlSession
from app.utils.db_redis import DBRedisSession

db = SQLAlchemy()
db_mysql = DBMysqlSession(db=db)
DBModel = db.Model

db_redis = DBRedisSession()

migrate = Migrate()
moment = Moment()
scheduler = APScheduler()


def init_app(app):
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('redis_tasks_queue', connection=app.redis)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    scheduler.init_app(app)
    scheduler.start()


from app.schedulers import *
