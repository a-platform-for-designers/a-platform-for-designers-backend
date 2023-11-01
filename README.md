# DesignCollab

## Описание проекта:

DesignCollab - это веб-платформа для дизайнеров.

## Используемые технологии:

Django: Django - это мощный фреймворк для создания веб-приложений на Python. Он предоставляет широкий спектр инструментов, включая маршрутизацию, шаблонизацию, аутентификацию и многое другое, что значительно упрощает процесс разработки веб-приложений.

Django REST framework: Django REST framework - это набор инструментов для создания REST API на Python. Он включает функционал для обработки различных форматов данных, аутентификации и многих других возможностей, что делает процесс создания REST API более эффективным и удобным.

Djoser: Djoser - это фреймворк для создания REST API, который специализируется на регистрации, аутентификации и управлении пользователями. Он предлагает функционал для работы с электронной почтой и множество других возможностей, что делает управление пользователями удобным и надежным.

DRF Spectacular: DRF Spectacular - это расширение для Django REST framework, предназначенное для создания схемы OpenAPI для REST API. Оно автоматически генерирует схему OpenAPI, что значительно облегчает процесс разработки и тестирования API. С помощью DRF Spectacular, вы можете легко создавать документацию для вашего API, а также использовать сгенерированную схему для автоматического тестирования.

Docker: Docker - это платформа для упаковки и развертывания приложений в контейнерах. Он позволяет разработчикам упаковывать приложения вместе с их зависимостями в контейнеры, которые могут быть запущены на любой платформе, где установлен Docker. Это значительно упрощает управление и развертывание приложений в различных средах.

wait-for-it.sh: wait-for-it.sh - это скрипт на языке Bash, который ожидает готовности сервера перед тем, как продолжить выполнение других команд. В контексте Docker, он может быть полезен для убеждениясь, что серверы внутри контейнеров готовы к работе перед запуском приложения. Это помогает избежать возможных ошибок из-за неготовности окружения перед началом работы приложения.

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

 - [ ] Запустить Docker из папки infra:
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
  - [ ] Git Bash из папки backend:
```
 dos2unix entrypoint.sh wait-for-it.sh
```
 - Ответ должен быть:

``` 
MINGW64 ~/a-platform-for-designers-backend/backend (main)   
dos2unix entrypoint.sh wait-for-it.sh
dos2unix: converting file entrypoint.sh to Unix format...
dos2unix: converting file wait-for-it.sh to Unix format...
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
docker-compose up -d
docker-compose exec backend python manage.py makemigrations users
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --noinput
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
    Pillow
    psycopg2-binary==2.9.3
    python-dotenv==0.21.0
    zipp==3.15.0
