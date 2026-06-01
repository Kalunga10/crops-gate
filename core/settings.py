from pathlib import Path
import os

# =========================
# BASE DIR
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-4h-e@i*#sm!n7)3jxh6p4ag9smn^pf_i=1wbnm+9v8@r-kd#o='
)

DEBUG = os.environ.get(
    'DEBUG',
    'True'
) == 'True'

ALLOWED_HOSTS = [

    '*',

    '.onrender.com',

    'localhost',

    '127.0.0.1',

]

# =========================
# CSRF
# =========================

CSRF_TRUSTED_ORIGINS = [

    'https://*.onrender.com',

    'https://*.ngrok-free.dev',

    'https://dorathy-uncravatted-nonoriginally.ngrok-free.dev',

]

# =========================
# INSTALLED APPS
# =========================

INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    # APPS DO SISTEMA

    'home',

    'usuarios',

    'motoristas',

    'agendamentos',

    'dashboard',

    'painel',

]

# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

# =========================
# URLS
# =========================

ROOT_URLCONF = 'core.urls'

# =========================
# TEMPLATES
# =========================

TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],

        },

    },

]

# =========================
# WSGI
# =========================

WSGI_APPLICATION = 'core.wsgi.application'

# =========================
# DATABASE
# =========================

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',

    }

}

# =========================
# PASSWORD VALIDATION
# =========================

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

# =========================
# LANGUAGE
# =========================

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = False

# =========================
# STATIC FILES
# =========================

STATIC_URL = '/static/'

STATICFILES_DIRS = [

    BASE_DIR / 'static',

]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = (

    'whitenoise.storage.CompressedManifestStaticFilesStorage'

)

# =========================
# MEDIA FILES
# =========================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# DEFAULT PK
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# LOGIN
# =========================

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/agendamentos/'

LOGOUT_REDIRECT_URL = '/login/'

# =========================
# RENDER
# =========================

SECURE_PROXY_SSL_HEADER = (

    'HTTP_X_FORWARDED_PROTO',

    'https'

)
