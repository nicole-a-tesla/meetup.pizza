from .base import *

DEBUG = True
HTMLVALIDATOR_FAILFAST = True
HTMLVALIDATOR_OUTPUT = 'stdout'

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'travis_ci_test',
    }
}

