#### start script

```bash

# development
flask run

# production
gunicorn --workers 4 --worker-class gthread runserver:app -b 0.0.0.0:18080

```