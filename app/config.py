import os

from starlette.config import Config
from starlette.datastructures import Secret

DEBUG = True
config = Config('.env')

DB_USERNAME = config("DB_USERNAME", cast=str, default="postgres")
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="postgres")
DB_HOST = config("DB_HOST", cast=str, default="localhost")
DB_PORT = config("DB_PORT", cast=str, default="5432")
DB_NAME = config("DB_NAME", cast=str, default="geo")
DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URL = f"postgresql://postgres:@localhost:5432/geo"

MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=20)

JWT_PRIVATE_KEY = config("JWT_PRIVATE_KEY", cast=str, default="june212021")
TEST_API_KEY = config("TEST_API_KEY", cast=str)
# will never expire (1000 weeks), belongs to test@foobar.com
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # one week
ALGORITHM = "HS256"