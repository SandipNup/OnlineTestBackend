import os
from config.settings.common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gtiw@sn^ex7yz8cno4zooj-^9hx!=d^xm=ka3=iaux6o+o5q#m'

# Do not forget to change this in production
# Just for production purposes
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'asdf1234',
        # The host is the name of database service in docker-compose.yml
        'HOST': 'postgresdb',
        'PORT': 5432
    }
}

