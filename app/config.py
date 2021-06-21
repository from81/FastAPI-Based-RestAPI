import os

from starlette.config import Config
from starlette.datastructures import Secret

config = Config('.env')

DB_USERNAME = config("DB_USERNAME", cast=str, default="postgres")
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="postgres")
DB_HOST = config("DB_HOST", cast=str, default="localhost")
DB_PORT = config("DB_PORT", cast=str, default="5432")
DB_NAME = config("DB_NAME", cast=str, default="geo")
JWT_PRIVATE_KEY = config("JWT_PRIVATE_KEY", cast=str, default="june212021")

DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
# MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT = 5
MAX_CONNECTIONS_COUNT = 100

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # one week
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJrYWl5aGlyb3RhQGdtYWlsLmNvbSIsImV4cCI6MTYyNDg3MzAzNX0.bE9CiNCp7rQXBq9jXtY7lkSm5fpbMrFUncF1E4yRMbs"