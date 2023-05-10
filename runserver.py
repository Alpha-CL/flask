import os

from dotenv import load_dotenv
from app import create_app

FLASK_ROOT_DIR = os.getenv("FLASK_ROOT_DIR")
load_dotenv(os.path.join(FLASK_ROOT_DIR, '.flaskenv'))

app = create_app()

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST')
    port = int(os.getenv('FLASK_RUN_PORT'))
    app.run(host, port, debug=True, threaded=True)
