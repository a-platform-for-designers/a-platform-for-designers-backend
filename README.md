# DesignCollab

## Описание проекта:

DesignCollab - это веб-платформа для дизайнеров, которая объединяет в себе два основных компонента: backend и frontend. Backend создан на языке программирования Python с использованием фреймворков Django и Django REST framework. Frontend, в свою очередь, разработан на языке JavaScript с применением библиотеки React.

## Используемые технологии:

Django: Это мощный фреймворк для создания веб-приложений на Python. Django предоставляет разнообразные инструменты, включая маршрутизацию, шаблонизацию, аутентификацию и многое другое, что упрощает процесс разработки веб-приложений.

Django REST framework: Этот фреймворк предоставляет инструменты для создания REST API на языке Python. Django REST framework включает в себя функционал для обработки форматов данных, аутентификации и многие другие возможности, делая процесс создания REST API эффективным и удобным.

Djoser: Djoser – это фреймворк для создания REST API, специализирующийся на регистрации, аутентификации и управлении пользователями. Он обладает функционалом для работы с электронной почтой и множеством других возможностей, что делает управление пользователями удобным и надежным.

DRF Spectacular: Этот фреймворк основан на Django REST framework и предназначен для создания схемы OpenAPI для вашего REST API. DRF Spectacular автоматически генерирует схему OpenAPI, облегчая процесс разработки и тестирования API.

Docker: Docker – это платформа для упаковки и разворачивания приложений в контейнерах. Она позволяет разработчикам упаковывать приложения и их зависимости в контейнеры, которые могут быть запущены на любой платформе, где установлен Docker. Это облегчает управление и развертывание приложений в различных средах.

wait-for-it.sh: Это скрипт на языке Bash, который ожидает готовности сервера перед тем, как продолжить выполнение других команд. В контексте Docker, он может быть полезен для убеждениясь, что серверы внутри контейнеров готовы к работе перед запуском приложения. Это помогает избежать возможных ошибок из-за неготовности окружения перед началом работы приложения.

## Запуск проекта через Docker(localhost):

Для запуска проекта необходимо выполнить следующие шаги:

 - [ ] Клонировать репозиторий:
```
git clone https://github.com/a-platform-for-designers/a-platform-for-designers-backend.git
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

 - При сборке контейнеров файлы entrypoint.sh и wait-for-it.sh должны быть в формате Unix, а не в формате DOS.
 Если после сборки контейнер не видит их, вы можете использовать утилиту dos2unix для конвертации файлов в формат Unix. Если у вас установлен Git Bash или WSL на Windows, вы можете выполнить следующую команду:
  - [ ] Git Bash:
```
 dos2unix entrypoint.sh wait-for-it.sh
```

 - При сборке контейнеров в файле entrypoint.sh прописаны команды, которые можно отредактировать:

команды в entrypoint.sh:

> Выполняем миграции и загружаем данные:
> 
> python manage.py makemigrations users
> 
> python manage.py migrate
> 
> python manage.py collectstatic --no-input

 - Список полезных команд:
 
```
docker compose up -d
docker compose exec backend python manage.py makemigrations users
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py collectstatic --noinput
```

 - requirements.txt:
 
    Django==4.2.1
    django-cors-headers==3.11.0
    django-colorful==1.3
    django-filter==22.1
    djangorestframework==3.14.0
    djoser==2.1.0
    drf-extra-fields==3.5.0
    drf-spectacular==0.25.0
    flake8==6.0.0
    gunicorn==20.1.0
    importlib-metadata==4.12.0
    Markdown==3.4.1
    psycopg2-binary==2.9.3
    python-dotenv==0.21.0
    zipp==3.15.0
