#!/usr/bin/env bash
set -o errexit

cd cmpes
python manage.py migrate --noinput
gunicorn config.wsgi:application
