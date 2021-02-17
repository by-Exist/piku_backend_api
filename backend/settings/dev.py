from .common import *
import environ


# set casting default value
env = environ.Env(
    # DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env()

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
