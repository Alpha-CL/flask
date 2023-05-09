import os

from dotenv import load_dotenv
from gevent import pywsgi
from app import create_app

app = create_app()

FLASK_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['FLASK_ROOT_DIR'] = FLASK_ROOT_DIR

load_dotenv(os.path.join(FLASK_ROOT_DIR, '.env'))
load_dotenv(os.path.join(FLASK_ROOT_DIR, '.flaskenv'))


if __name__ == '__main__':
    FLASK_HOST = os.getenv('FLASK_RUN_HOST')
    FLASK_PORT = int(os.getenv('FLASK_RUN_PORT'))
    server = pywsgi.WSGIServer((FLASK_HOST, FLASK_PORT), app)
    server.serve_forever()
