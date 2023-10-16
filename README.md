# Backend
# Онлайн-платформа для дизайнеров (бэкенд)

## Описание проекта:

Платформа для дизайнеров

## Технологии:

- Django - это фреймворк для создания веб-приложений на языке Python. Он предоставляет множество инструментов и библиотек для создания веб-приложений, включая маршрутизацию, шаблонизацию, аутентификацию и многое другое.

- Django REST framework - это фреймворк для создания REST API на языке Python. Он предоставляет множество инструментов и библиотек для создания REST API, включая поддержку форматов данных, аутентификацию и многое другое.

- Djoser - это фреймворк для создания REST API для регистрации, аутентификации и управления пользователями. Он предоставляет множество инструментов и библиотек для создания REST API для регистрации, аутентификации и управления пользователями, включая поддержку электронной почты и многое другое.

- Docker - это платформа для разработки, доставки и запуска приложений в контейнерах. Она позволяет упаковывать приложения и их зависимости в контейнеры, которые могут быть запущены на любой платформе, где установлен Docker.

## Запуск проекта через Docker(localhost):

Для запуска проекта необходимо выполнить следующие шаги:

 - [ ] Клонировать репозиторий:
```
git clone
```

 - [ ] Переименовать файл example.env в .env и заполнить его своими
       данными:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=poostgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost/db
DB_PORT=5432
SECRET_KEY='secretgenerate'
DEBUG = True
```

> Генератор секретного ключа: infra/secretgenerate.py

 - [ ] Запустить Docker:
```
 docker-compose up -d
```

 - [ ] Зарегистрировать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```

 - [ ] Запустить проект:

 
http://localhost/

 - [ ] После запуска проекта будут доступны следующие ссылки(API):

> Swagger UI:

http://localhost/api/schema/swagger-ui/

> ReDoc от DRF Spectacular:

http://localhost/api/schema/redoc/

> ReDoc проекта:

http://localhost/api/docs/redoc.html

> Скачать схему проекта можно по ссылке:

http://localhost/api/schema/


### **Дополнительная информация:**



 - Список полезных команд:
 
```
docker compose up -d

```

- requirements.txt:
 
Django==4.2.1
djoser==2.1.0
django-cors-headers
django-filter==22.1
drf-extra-fields==3.5.0
drf-spectacular
djangorestframework==3.14.0
flake8==6.0.0
gunicorn==20.1.0
psycopg2-binary==2.9.3
python-dotenv==0.21.0
zipp==3.15.0