# flask service


#### start script

```bash


# development
flask run

# production
gunicorn --workers 4 -b :8181 --worker-class gthread --access-logfile - --error-logfile - runserver:app


```

#### docker run

```bash


docker run \
  -itd --name test \
  -p 8181:8181 \
  -e SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:password@localhost:3306 \
  -e REDIS_URL=redis://:password@localhost:6379/0 \
  alpha92/flask-service:1.0


```