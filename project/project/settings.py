import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=v+1e!x(kof(^#cqz%!y5y9o7kgpwwwfnp$f_(0@d-$ld7&p=q"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


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

    # my apps
    'accounts_app',
    'appeals_app',
    'main_app',
    'about_app',
    'cyber_security_app',
    'news_app',
    'contacts_app',
    'cooperation_app',
    'legislation_app',
    'messages_app'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(os.path.dirname(BASE_DIR), 'templates')],
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
        'NAME': 'cert_gov',  # Имя вашей базы данных
        'USER': 'ular',  # Имя вашего пользователя
        'PASSWORD': 'admin',  # Ваш пароль
        'HOST': '127.0.0.1',  # Хост, на котором работает PostgreSQL
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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

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

USE_TZ = True

STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)



STATICFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), 'static-backend'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static-root')
STATIC_URL = '/static-root/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
