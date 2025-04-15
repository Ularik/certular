import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=v+1e!x(kof(^#cqz%!y5y9o7kgpwwwfnp$f_(0@d-$ld7&p=q"

import dotenv
dotenv.load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['213.109.67.179', 'cert.gov.kg', '10.100.191.9', '10.100.191.8', '127.0.0.1', 'localhost']


# Application definition

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
    'django_recaptcha',
    'rest_framework',

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
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),  # Имя вашей базы данных
        'USER': os.getenv('POSTGRES_USER'),  # Имя вашего пользователя
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),  # Ваш пароль
        # 'HOST': 'db',  # docker
        'HOST': 'localhost',  # Хост, на котором работает PostgreSQL
        'PORT': '5432',  # Порт (по умолчанию 5432)
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
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

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')

    # Если ты за прокси:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

else:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, '..', 'static'),
    ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

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
        'news_app': {
            'level': 'INFO',
            'handlers': ['console',]
        }
    },
}

DJANGO_DB_LOGGER_ENABLE_FORMATTER = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.cert.gov.kg'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
APPEAL_EMAIL = ''

# captcha google
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')