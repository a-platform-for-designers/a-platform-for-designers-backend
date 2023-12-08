#!/bin/bash

./wait-for-it.sh db:5432 --timeout=30

python manage.py makemigrations users
python manage.py makemigrations job
python manage.py migrate
# python manage.py load_data
python manage.py collectstatic --no-input

exec gunicorn designers.wsgi:application --bind 0:8000
