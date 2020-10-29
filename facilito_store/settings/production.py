from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['facilito-store.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd9glaubtgdcig0',
        'USER': 'bfaockdhmoqcxa',
        'PASSWORD': 'a0d2525bd39821901a2ba32dda333d0c9a096de3eac0bc9cf7213267b40bb348',
        'HOST':'ec2-3-218-75-21.compute-1.amazonaws.com',
        'DATABASE_PORT':'5432',
   }
}