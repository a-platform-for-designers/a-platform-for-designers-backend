#!/bin/bash

# Ожидаем доступности базы данных
./wait-for-it.sh db:5432 --timeout=30

# Выполняем миграции и загружаем данные
python manage.py makemigrations users
python manage.py migrate
python manage.py collectstatic --no-input

# Запускаем сервер
exec gunicorn designers.wsgi:application --bind 0:8000


# Импортируем данные из csv
python manage.py direction_import_csv
python manage.py sphere_import_csv
python manage.py skills_import_csv
python manage.py tools_import_csv
python manage.py country_import_csv
