import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
env_path = Path("../infra") / '.env'

load_dotenv()

SECRET_KEY = str(os.getenv('SECRET_KEY'))

if not SECRET_KEY:
    raise ValueError('SECRET_KEY не установлен')

DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = [
    'localhost',
    'backend',
    '127.0.0.1',
    '91.226.81.209'
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://backend',
    'http://127.0.0.1',
    'https://127.0.0.1',
    'http://91.226.81.209',
    'https://91.226.81.209'
]

INSTALLED_APPS = [

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'drf_spectacular',
    'corsheaders',

    # Local apps
    'users',
    'api',
    'job',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'designers.urls'

# TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'designers.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv(
#             'DB_ENGINE',
#             default='django.db.backends.postgresql'
#         ),
#         'NAME': os.getenv('DB_NAME', default='postgres'),
#         'USER': os.getenv('POSTGRES_USER', default='postgres'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
#         'HOST': os.getenv('DB_HOST', default='db'),
#         'PORT': os.getenv('DB_PORT', default='5432'),
#         'OPTIONS': {
#             'client_encoding': 'UTF8'
#         },
#     }
# }



# Password validation

AUTH_PWD_MODULE = "django.contrib.auth.password_validation."

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{AUTH_PWD_MODULE}UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{AUTH_PWD_MODULE}MinimumLengthValidator",
    },
    {
        "NAME": f"{AUTH_PWD_MODULE}CommonPasswordValidator",
    },
    {
        "NAME": f"{AUTH_PWD_MODULE}NumericPasswordValidator",
    },
]

# Internationalization

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# http://localhost/api/users/activation/
# http://localhost/api/users/reset_password/
DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'SEND_ACTIVATION_EMAIL': False,
    'SEND_CONFIRMATION_EMAIL': False,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'reset/{uid}/{token}',
    'SERIALIZERS': {
        'user_create': (
            'api.serializers.UserProfileCreateSerializer'  
        ),
        'user': (
            'api.serializers.UserProfileSerializer'
        ),
        'current_user': (
            'api.serializers.UserProfileSerializer'
        ),
    },

    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
        'user_list': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    },
}


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

SPECTACULAR_SETTINGS = {
    'TITLE': 'DesignCollab API',
    'DESCRIPTION': 'Схема API проекта DesignCollab',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False
}

AUTH_USER_MODEL = 'users.User'


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
