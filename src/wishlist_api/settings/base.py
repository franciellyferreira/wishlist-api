import os

import dj_database_url

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'USE_MAKE_COMMAND_TO_GENERATE_SECRET_KEY'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
))))

DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///wishlist.db')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

OUTSIDE_APPS = [
    'rest_framework',
]

CHALLENGE_APPS = [
    'wishlist_api.client.apps.ClientConfig',
    'wishlist_api.wishlist.apps.WishlistConfig',
]

INSTALLED_APPS = DJANGO_APPS + OUTSIDE_APPS + CHALLENGE_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wishlist_api.urls'

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

WSGI_APPLICATION = 'wishlist_api.wsgi.application'

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URI)
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # noqa
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'wishlist_api.pagination.CustomPagination'
}


API_MAGALU_PRODUCT = {
    'API_MAGALU_PRODUCT': {
        'url': 'http://challenge-api.luizalabs.com',
        'timeout': 10
    }
}
