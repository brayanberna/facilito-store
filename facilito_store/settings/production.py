from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['facilito-store.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dr4civo2fkbk',
        'USER': 'ocwwbxgtyktzyu',
        'PASSWORD': 'c4c1fd9841b8596e6d36dfa2fb2e21f6ba3c7330d1585dd150422e2c6151fd9f',
        'HOST':'ec2-23-20-70-32.compute-1.amazonaws.com',
        'DATABASE_PORT':'5432',
   }
}