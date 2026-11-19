import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
import dotenv
from django.core.exceptions import ImproperlyConfigured
dotenv.load_dotenv()


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ('true', '1', 'yes', 'on')


def env_list(name):
    # Принимает "a,b" и формат Python-списка "['a', 'b']"
    value = os.getenv(name, '').strip().strip('[]')
    return [item.strip().strip('\'"') for item in value.split(',') if item.strip().strip('\'"')]


MODE = os.getenv("MODE", "").strip().upper()
DB_HOSTS = {
    "LOCAL": os.getenv("POSTGRES_HOST"),
    "DOCKER": os.getenv("POSTGRES_HOST_DOCKER"),
}
if MODE not in DB_HOSTS:
    raise ImproperlyConfigured(f"MODE в .env должен быть LOCAL или DOCKER, сейчас: {MODE!r}")

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = env_bool("DEBUG")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    #another modules
    'tinymce',
    'parler',
    'rest_framework',
    'ninja_extra',

    # my apps
    'db_logger',
    'accounts_app',
    'appeals_app',
    'main_app',
    'about_app',
    'cyber_security_app',
    'news_app',
    'contacts_app',
    'cooperation_app',
    'legislation_app',
    'messages_app',
    'reports_app',
    'e_learning',
    'bulletins',
    'szi'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "project.middleware.RateLimitMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'project.middleware.LanguageMiddleware',
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"
AUTH_USER_MODEL = 'accounts_app.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': DB_HOSTS[MODE],
        'PORT': os.getenv("POSTGRES_PORT"),
        'TEST': {
            'NAME': '',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REDIS_HOST = os.getenv('REDIS_HOST') if MODE == "LOCAL" else os.getenv('REDIS_HOST_DOCKER')
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{os.getenv('REDIS_PORT')}",
        # "LOCATION": "redis://127.0.0.1:6380",  # docker container

    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
from django.utils.translation import gettext_lazy as _


LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
    ("ky", _("Kyrgiz"))
]

LOCALE_PATHS = [
	os.path.join(BASE_DIR, 'locale'),
]


TIME_ZONE = "Asia/Bishkek"

PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'ky'},
        {'code': 'ru'},
    ),
    'default': {
        'fallbacks': ['ru'],
        'hide_untranslated': False,
    }
}

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

# static/ — исходники, staticfiles/ — результат collectstatic (раздаётся nginx)
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGS_DIR = os.path.join(BASE_DIR, '../logs/')

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'console_lite': {
            'format': '%(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
        'db_logger': {
            'format': '%(name)-12s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'console_lite': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_lite'
        },
        'db_logger': {
            'level': 'DEBUG',
            'formatter': 'db_logger',
            'class': 'db_logger.db_log_handler.DatabaseLogHandler'
        }
    },
    'loggers': {
        'django': {
            'level': 'WARNING',
            'handlers': ['console']
        },
        'reports_app': {
            'level': 'INFO',
            'handlers': ['console_lite', 'db_logger']
        },
        'accounts_app': {
            'level': 'INFO',
            'handlers': ['console_lite', 'db_logger']
        },
        'messages_app': {
            'level': 'INFO',
            'handlers': ['console_lite', 'db_logger']
        },
        'news_app': {
            'level': 'INFO',
            'handlers': ['console',]
        }
    },
}

DJANGO_DB_LOGGER_ENABLE_FORMATTER = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
APPEAL_EMAIL = os.getenv("APPEAL_EMAIL", '')

# URL, на который дополнительно пересылается каждая заявка об инциденте (POST, multipart/form-data).
# Пустое значение отключает пересылку.
MESSAGE_SEND_ADDRESS = os.getenv("MESSAGE_SEND_ADDRESS", "").strip()
