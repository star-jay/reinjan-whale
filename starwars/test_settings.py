# Settings to apply when running tests

import environ

from .settings import *  # noqa

env = environ.Env()
environ.Env.read_env()

DATABASES = {
    'default': env.db(
        'TEST_DATABASE_URL',
        default='postgres:///heartguide'),
}
