import asyncio
from typing import Optional
import datetime
import json
import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2
import uvicorn

from services.neighborhood_service import NeighborhoodService

with open('../credentials_dev.json') as f:
    credentials = json.load(f)

orig_token = credentials['token']

conn = psycopg2.connect(f"postgresql://{credentials['username']}:{credentials['password']}@{credentials['db_host']}:{credentials['port']}/{credentials['database']}")

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
def neighborhood(lat: float, lon: float, token: str):
    if token == orig_token:
        cur = conn.cursor()
        geojs = NeighborhoodService.get_neighborhood(cur, lat, lon)
        return geojs
    else:
        # TODO
        return None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
