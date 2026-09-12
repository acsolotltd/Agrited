from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-332iif*t7o32u)!-cwjgf02f2c)+f434p0dnb_fwft)48-+h%k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not True

ALLOWED_HOSTS = ["*", "0.0.0.0", "agrited.pythonanywhere.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
     "anymail",
     "tailwind",
      "django_htmx",
      "theme",
    "apps.core.apps.CoreConfig",
    "apps.accounts.apps.AccountsConfig",
    "apps.orders.apps.OrdersConfig",
    "apps.subscribe.apps.SubscribeConfig",
     'huey.contrib.djhuey',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
        "django_htmx.middleware.HtmxMiddleware",

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    "hx-request",
    "hx-target",
    "hx-current-url",
    "hx-trigger",
    "hx-prompt",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080", # Replace with your actual HTML host URL
    "http://127.0.0.1:8000",
    "0.0.0.0",
    "https://itsupport1-agrited.netlify.app",            # Good to keep for local frontend testing
]
ROOT_URLCONF = 'controller.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"src/templates/"],
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

WSGI_APPLICATION = 'controller.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

AUTH_USER_MODEL="accounts.EmailBasedUser"
STATIC_URL="/static/"

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
else:
    STATICFILES_DIRS = [BASE_DIR / "apps/css", BASE_DIR / "src/assets",]
    INSTALLED_APPS += ["django_browser_reload"]
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

TAILWIND_APP_NAME = "theme"


NPM_BIN_PATH = "npm.cmd"

HUEY = {
    'huey_class': 'huey.SqliteHuey',
    #'backend': 'huey.backends.sqlite_backend',  # required.
    'name': 'Agrited-BG-Task',
     'results': True,
    'store_none': False,
    'immediate': False,
    #'connection': {'location': BASE_DIR/'tasks.db'},
    #'always_eager': False, # Defaults to False when running via manage.py run_huey
    # Options to pass into the consumer when running ``manage.py run_huey``
    #'consumer_options': {'workers': 4,  'worker_type': 'thread'},
}


BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
if not BREVO_API_KEY:
    raise ImproperlyConfigured("CRITICAL: BREVO_API_KEY is completely missing from the environment!")
MAILERS = {
    "default": {
        "BACKEND": "anymail.backends.brevo.EmailBackend",
        "OPTIONS": {
            "api_key": BREVO_API_KEY,
        },
    }
}
ANYMAIL = {
    "BREVO_API_KEY":  BREVO_API_KEY,

}
DEFAULT_FROM_EMAIL = "noreply@ylocalhost.com"
SERVER_EMAIL = "errors@localhost.com"