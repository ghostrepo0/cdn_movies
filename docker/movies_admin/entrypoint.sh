#!/bin/sh

if [ "${POSTGRES_DB}" = "movies_database" ]
then
    echo "launching postgresql database..."

    while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
      sleep 0.1
    done

    echo "postgresql started"
fi

exec "$@"
