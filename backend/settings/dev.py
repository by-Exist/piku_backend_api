from .common import *
import environ
import socket

LOCAL_ENV_PATH = "backend/settings/local.env"
USE_GITHUB_WORKFLOW_ENV = os.environ.get("GITHUB_WORKFLOW", False)

if USE_GITHUB_WORKFLOW_ENV:
    # use github workflow env
    env = environ.Env(
        DJANGO_DEBUG=(bool, os.environ.get("DJANGO_DEBUG")),
        DJANGO_SECRET_KEY=(str, os.environ.get("DJANGO_SECRET_KEY")),
        DJANGO_ALLOWED_HOSTS=(str, os.environ.get("DJANGO_ALLOWED_HOSTS")),
        DJANGO_DATABASE_URL=(str, os.environ.get("DJANGO_DATABASE_URL")),
    )
else:
    # use .env file
    env = environ.Env()
    with open(BASE_DIR / LOCAL_ENV_PATH) as env_file:
        environ.Env.read_env(env_file)

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [*env("DJANGO_ALLOWED_HOSTS").split(" ")]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    # "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
    "default": env.db("DJANGO_DATABASE_URL")
}

# INTERNAL_IPS - Debug Toolbar need value with Docker
# https://stackoverflow.com/questions/26898597/django-debug-toolbar-and-docker
INTERNAL_IPS = [socket.gethostbyname(socket.gethostname())[:-1] + "1"]

# LOCAL EMAIL - https://docs.djangoproject.com/en/3.1/topics/email/#file-backend
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / PROJECT_NAME / "_email"


# Dev Drf_spectacular Settings
SPECTACULAR_SETTINGS = {
    # Schema metadata
    "TITLE": "Developer's Swagger",
    "DESCRIPTION": "개발 용도로 사용되는 Swagger입니다.",
    "VERSION": "0.0.1",
    # Useful settings
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "DISABLE_ERRORS_AND_WARNINGS": False,
}
