from starlette.config import Config
from starlette.datastructures import Secret

"""
The order in which configuration values are read is:
1. From an environment variable.
2. From the ".env" file.
3. The default value given in config.
"""

DEBUG = False
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week
ALGORITHM = "HS256"

config = Config('.env')

DB_USERNAME = config("DB_USERNAME", cast=str, default="postgres")
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="postgres")
DB_HOST = config("DB_HOST", cast=str, default="localhost")
DB_PORT = config("DB_PORT", cast=str, default="5432")
DB_NAME = config("DB_NAME", cast=str, default="geo")

DB_URL = config(
    "DB_URL",
    cast=str,
    default=f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

n = len(DB_HOST) // 2
DB_HOST_ENCRYPT = ('*' * n) + DB_HOST[n:]
DB_URL_ENCRYPT = f"postgresql://{DB_USERNAME}:{'*' * len(str(DB_PASSWORD))}@{DB_HOST_ENCRYPT}:{DB_PORT}/{DB_NAME}"

MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=20)

JWT_PRIVATE_KEY = config("JWT_PRIVATE_KEY", cast=Secret, default="june212021")
TEST_API_KEY = config("TEST_API_KEY", cast=Secret)
# will never expire (1000 weeks), belongs to test@foobar.com
