#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "launching postgresql database..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "postgresql started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"