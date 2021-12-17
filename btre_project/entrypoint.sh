#!/usr/bin/env sh

  set -e

  if [ "$PG_HOST" = "postgres" ]
  then
      echo "Waiting for postgres"
      while ! nc -z "$PG_HOST" "$PG_PORT"; do
        sleep 0.1
      done
      echo "PgSQL started"
  fi


  python manage.py collectstatic --noinput



  exec "$@"
