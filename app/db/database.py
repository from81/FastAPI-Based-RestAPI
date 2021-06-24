from typing import AsyncGenerator

from asyncpg.connection import Connection
from asyncpg.pool import Pool
from fastapi import Depends
from starlette.requests import Request

def _get_db_pool(request: Request) -> Pool:
    return request.app.state.pool

# https://github.com/tiangolo/fastapi/issues/679
# https://github.com/tiangolo/fastapi/issues/1921
async def _get_connection_from_pool(pool: Pool = Depends(_get_db_pool)) -> AsyncGenerator[Connection, None]:
    async with pool.acquire() as conn:
        yield conn