import asyncio
import datetime
from typing import Optional

import asyncpg
from asyncpg.exceptions import PostgresError
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
import uvicorn

from app.config import (
    DB_URL,
    DB_URL_ENCRYPT,
    MIN_CONNECTIONS_COUNT,
    MAX_CONNECTIONS_COUNT,
    DEBUG
)
from app.endpoint.neighborhood import neighborhood_router
from app.endpoint.apikey import apikey_router
from app.endpoint.token import token_router
from app.exceptions.exceptions import DBConnectionError, DBDisconnectError
from app.exceptions.handlers import exception_handlers

app = FastAPI(
    title="Geo RestAPI project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0",
    debug=DEBUG,
    exception_handlers=exception_handlers
)
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")
app.include_router(neighborhood_router, prefix="/neighborhood")
app.include_router(apikey_router, prefix="/apikey")
app.include_router(token_router, prefix="/token")


@app.on_event("startup")
async def startup():
    logger.info(f"Connecting to database -> {DB_URL_ENCRYPT}")

    try:
        app.state.pool = await asyncpg.create_pool(
            DB_URL,
            min_size=MIN_CONNECTIONS_COUNT,
            max_size=MAX_CONNECTIONS_COUNT,
        )
        logger.info("Connection established")
    except PostgresError as e:
        logger.warning(e)
        raise DBConnectionError from e
    except Exception as e:
        logger.warning(e)
        raise e


@app.on_event("shutdown")
async def shutdown():
    logger.info(f"Closing connection to database -> {DB_URL_ENCRYPT}")

    try:
        await app.state.pool.close()
        logger.info("Connection closed")
    except PostgresError as e:
        logger.warning(e)
        raise DBDisconnectError from e
    except Exception as e:
        logger.warning(e)
        raise e


@app.get("/")
def home():
    return JSONResponse(status_code=200, content={"message": "Welcome to GeoAPI"})


@app.get("/test")
def test():
    return JSONResponse(status_code=200, content={"message": "OK"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
