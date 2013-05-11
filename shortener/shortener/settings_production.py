# -*- coding: utf-8 -*-
from settings import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.pyscopg2',
        'NAME': 'shortener',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = [
    '.encurtador.com.br'
]