import asyncio
from typing import Optional
import datetime
import os
import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from services.neighborhood_service import NeighborhoodService

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = FastAPI(
    title="Geo RestAPI project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0",
)

@app.get("/")
async def root():
    dt = datetime.datetime.now()
    return {"message": "Hello World", "datetime": dt.strftime("%m/%d/%Y, %H:%M:%S")}

@app.get("/test")
def test():
    return JSONResponse(status_code=200, content={"message": "OK"})

@app.get("/neighborhood")
def neighborhood(lat: float, lon: float):
    geojs = NeighborhoodService.get_neighborhood(DB_URL, lat, lon)
    return geojs

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
