"""Project settings."""

import sys

from dynaconf import LazySettings


# --- BEGIN OF DYNACONF HEADER ---
settings = LazySettings(
    GLOBAL_ENV_FOR_DYNACONF='GALAXY',

)
# --- END OF DYNACONF HEADER ---

# ---------------------------------------------------------
# Django settings
# ---------------------------------------------------------

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_yasg',

    'galaxy_api.api',
    'galaxy_api.auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

]

ROOT_URLCONF = 'galaxy_api.urls'

# Authentication


AUTH_USER_MODEL = 'galaxy_auth.user'

# community v1/v2 style pagination with count/previous/next/results
# GALAXY_DEFAULT_PAGINATION = 'galaxy_api.api.pagination.PageNumberPagination'
# GALAXY_DEFAULT_PAGINATION_INSPECTOR = 'galaxy_api.api.drf_yasg_ext.PageNumberPaginationInspector'

# insights style pagination with meta/links/data
GALAXY_DEFAULT_PAGINATION = 'galaxy_api.api.pagination.InsightsStylePagination'
GALAXY_DEFAULT_PAGINATION_INSPECTOR = 'galaxy_api.api.drf_yasg_ext.IPP12RestResponsePagination',

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': GALAXY_DEFAULT_PAGINATION,
    'PAGE_SIZE': 100,

    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.TokenAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    # ),
}

SWAGGER_SETTINGS = {
   'DEFAULT_INFO': 'galaxy_api.urls.api_info',
   'DEFAULT_PAGINATOR_INSPECTORS': [
        'drf_yasg.inspectors.DjangoRestResponsePagination',
        'drf_yasg.inspectors.CoreAPICompatInspector',
        GALAXY_DEFAULT_PAGINATION_INSPECTOR,
   ],

}

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


WSGI_APPLICATION = 'galaxy_api.wsgi.application'

# Database

# AUTH_USER_MODEL = 'galaxy_api.CustomUser'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': settings.get('DB_NAME', 'galaxy'),
        'USER': settings.get('DB_USER', 'galaxy'),
        'PASSWORD': settings.get('DB_PASSWORD', ''),
        'HOST': settings.get('DB_HOST', 'localhost'),
        'PORT': settings.get('DB_PORT', ''),
    }
}


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

# ---------------------------------------------------------
# Third party libraries settings
# ---------------------------------------------------------

# ---------------------------------------------------------
# Application settings
# ---------------------------------------------------------

API_PATH_PREFIX = 'api'

# --- BEGIN OF DYNACONF FOOTER ---
settings.populate_obj(sys.modules[__name__])
# --- END OF DYNACONF FOOTER ---
