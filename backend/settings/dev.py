from .common import *
import environ

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
