import os

from starlette.config import Config
from starlette.datastructures import Secret

if os.path.exists('../.env'):
    config = Config('../.env')
else:
    config = None

if config:
    DB_USERNAME = config("DB_USERNAME", cast=str)
    DB_PASSWORD = config("DB_PASSWORD", cast=Secret)
    DB_HOST = config("DB_HOST", cast=str, default="localhost")
    DB_PORT = config("DB_PORT", cast=str, default="5432")
    DB_NAME = config("DB_NAME", cast=str)
    JWT_PRIVATE_KEY = config("JWT_PRIVATE_KEY", cast=str)
else:
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    JWT_PRIVATE_KEY = os.getenv('JWT_PRIVATE_KEY')

DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
# MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT = 5
MAX_CONNECTIONS_COUNT = 100

JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # one week