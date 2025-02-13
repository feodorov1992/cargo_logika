import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(),
    )
)
CSRF_TRUSTED_ORIGINS = [f'https://{i}' for i in ALLOWED_HOSTS]
# Application definition

INSTALLED_APPS = [
    'app.apps.CargoLogikaAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'captcha',
    'app_auth',
    'core',
    'log_cats',
    'logistics',
    'dynamic_docs',
    'mailer',
    'clients_area'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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
                'app.context_processors.app_settings',
                'app.context_processors.meta_tags',
            ],
            'libraries': {
                'pdf_static': 'app.templatetags.pdf_static'
            },

        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'app_auth.User'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'static/static/'
MEDIA_URL = 'static/media/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_ROOT = '/vol/web/media/'
STATIC_ROOT = '/vol/web/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

XDG_RUNTIME_DIR = '/tmp/runtime-app'

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = bool(int(os.environ.get('EMAIL_USE_SSL', 1)))
EMAIL_ACCOUNTS_ADDRESS = os.environ.get('EMAIL_ACCOUNTS_ADDRESS')
EMAIL_ADMIN_ADDRESS = os.environ.get('EMAIL_ADMIN_ADDRESS')
EMAIL_LOGIST_ADDRESS = os.environ.get('EMAIL_LOGIST_ADDRESS')
MAIN_PHONE = os.environ.get('MAIN_PHONE')
MAIN_PHONE_RAW = ''.join(filter(lambda x: x.isnumeric(), MAIN_PHONE))
FACT_ADDRESS = os.environ.get('FACT_ADDRESS')
YANDEX_MAPS_LINK = os.environ.get('YANDEX_MAPS_LINK')
YANDEX_MAPS_API_LINK = os.environ.get('YANDEX_MAPS_API_LINK')
INITIAL_ORDER_NUMBER = int(os.environ.get('INITIAL_ORDER_NUMBER'))
DADATA_TOKEN = os.environ.get('DADATA_TOKEN')
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
