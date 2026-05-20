#!/bin/sh
set -e

echo "Ожидание базы данных..."
python << 'PY'
import os
import sys
import time

import psycopg2

for i in range(30):
    try:
        psycopg2.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ.get("POSTGRES_HOST", "db"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
        ).close()
        break
    except psycopg2.OperationalError:
        if i == 29:
            sys.exit(1)
        time.sleep(1)
PY

python manage.py migrate --noinput
python manage.py seed_data
python manage.py collectstatic --noinput

exec "$@"
