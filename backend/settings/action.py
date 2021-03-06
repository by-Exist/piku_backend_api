from .common import *
import environ

DEBUG = True
ACTION_ENV_PATH = "backend/settings/action.env"

env = environ.Env()
with open(BASE_DIR / ACTION_ENV_PATH) as env_file:
    environ.Env.read_env(env_file)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [*env("DJANGO_ALLOWED_HOSTS").split(",")]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    # "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
    "default": env.db("DJANGO_DATABASE_URL")
}

# INTERNAL_IPS - needed Debug Toolbar for Docker
# https://stackoverflow.com/questions/26898597/django-debug-toolbar-and-docker
INTERNAL_IPS = type(str("c"), (), {"__contains__": lambda *a: True})()


# LOCAL EMAIL - https://docs.djangoproject.com/en/3.1/topics/email/#file-backend
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / PROJECT_NAME / "_email"
