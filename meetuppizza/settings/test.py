from .base import *

DEBUG = True
HTMLVALIDATOR_ENABLED = True
HTMLVALIDATOR_OUTPUT = 'stdout'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'localpizzatestdb',
    }
}
