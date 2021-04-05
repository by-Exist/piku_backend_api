from .common import *
import environ

DEBUG = False
PROD_SECRET_FILE_PATH = "/run/secrets/prod.env"  # container secret file path

env = environ.Env()
with open(BASE_DIR / PROD_SECRET_FILE_PATH) as env_file:
    environ.Env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [*env("DJANGO_ALLOWED_HOSTS").split(" ")]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {"default": env.db("DJANGO_DATABASE_URL")}
