from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'travis_ci_test',
    }
}

