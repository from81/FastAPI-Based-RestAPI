import asyncio
import datetime

import asyncpg
from asyncpg.connection import Connection
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn

from config import (
    DB_URL,
    MIN_CONNECTIONS_COUNT,
    MAX_CONNECTIONS_COUNT
)
from database import _get_connection_from_pool
from models.feature import FeatureCollection
from services.neighborhood_service import NeighborhoodService

app = FastAPI(
    title="Geo RestAPI project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0",
)

@app.on_event("startup")
async def startup():
    logger.info(f"Connecting to {DB_URL}")

    try:
        app.state.pool = await asyncpg.create_pool(
            DB_URL,
            min_size=MIN_CONNECTIONS_COUNT,
            max_size=MAX_CONNECTIONS_COUNT,
        )
        logger.info("Connection established")
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Closing connection to database")

    try:
        await app.state.pool.close()
        logger.info("Connection closed")
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")

@app.get("/")
def root():
    dt = datetime.datetime.now()
    return {"message": "Hello World", "datetime": dt.strftime("%m/%d/%Y, %H:%M:%S")}

@app.get("/test")
def test():
    return JSONResponse(status_code=200, content={"message": "OK"})

@app.get("/neighborhood", response_model=FeatureCollection)
async def neighborhood(lat: float, lon: float, conn: Connection = Depends(_get_connection_from_pool)):
    return await NeighborhoodService.get_neighborhood(conn, lat, lon)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
