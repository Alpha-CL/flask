#### start script

```bash

# development
flask run

# production
gunicorn --workers 4 -b :18080 --worker-class gthread --access-logfile - --error-logfile - runserver:app

```
