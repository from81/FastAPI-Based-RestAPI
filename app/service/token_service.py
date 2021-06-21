from datetime import datetime, time, timedelta

from asyncpg.connection import Connection
from asyncpg.exceptions import UniqueViolationError
import jwt
from jwt.exceptions import ExpiredSignatureError
from loguru import logger

from app.config import JWT_PRIVATE_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
# from app.exceptions import DoesNotExistException
from app.queries import queries

class TokenService:
    @staticmethod
    @logger.catch
    async def create_table_if_not_exists(conn: Connection):
        await queries.create_apikey_table(conn)

    @staticmethod
    @logger.catch
    def issue_token(conn: Connection, email: str) -> str:
        payload = {
            'iss': email,
            'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        encoded = jwt.encode(payload, JWT_PRIVATE_KEY, algorithm=ALGORITHM)
        return encoded

    @staticmethod
    @logger.catch
    async def register_token(conn: Connection, email: str, token: str) -> bool:
        await TokenService.create_table_if_not_exists(conn)
        
        # delete any previously issued tokens
        await queries.delete_apikey(conn, email)

        try:
            ret = await queries.insert_apikey(conn, email, token)
            return True
        except UniqueViolationError as e:
            logger.warning("Email and token already exists.")
            # TODO: handle exception if token and email already exists -> show message in frontend
            return True
        except Exception as e:
            logger.warning(e)
            return False

    @staticmethod
    @logger.catch
    async def verify_token(conn: Connection, token: str) -> bool:
        await TokenService.create_table_if_not_exists(conn)
        ret = await queries.verify_apikey(conn, token)
        try:
            ret = ret[0]
            if token == ret['token']:
                decoded: dict = jwt.decode(ret['token'], JWT_PRIVATE_KEY, algorithms=ALGORITHM)
                return True
        except IndexError as e:
            logger.warning(e)
            return False
        # except DoesNotExistException as e:
        #     pass
        except ExpiredSignatureError as e:
            #TODO redirect user to "token/" for updating apikey
            logger.warning(e)
            return False
        except Exception as e:
            logger.warning(e)
            return False