#!/bin/bash
source venv/bin/activate
# init database
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
# run start app
exec gunicorn --workers 4 -b :18080 --worker-class gthread --access-logfile - --error-logfile - runserver:app
