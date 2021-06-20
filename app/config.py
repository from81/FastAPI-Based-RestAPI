import os

from starlette.config import Config
from starlette.datastructures import Secret

if os.path.exists('../.env'):
    config = Config('../.env')
    DB_USERNAME = config("DB_USERNAME", cast=str)
    DB_PASSWORD = config("DB_PASSWORD", cast=Secret)
    DB_HOST = config("DB_HOST", cast=str, default="localhost")
    DB_PORT = config("DB_PORT", cast=str, default="5432")
    DB_NAME = config("DB_NAME", cast=str)
else:
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

MIN_CONNECTIONS_COUNT = 0
MAX_CONNECTIONS_COUNT = 1000