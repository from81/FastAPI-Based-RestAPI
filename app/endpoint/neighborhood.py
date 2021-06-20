from fastapi import APIRouter, Depends
from asyncpg.connection import Connection

from database import _get_connection_from_pool
from model.feature import FeatureCollection
from service.neighborhood_service import NeighborhoodService

neighborhood_router = APIRouter()

@neighborhood_router.get("/", response_model=FeatureCollection, response_model_exclude_unset=True)
async def neighborhood(
    lat: float, lon: float, conn: Connection = Depends(_get_connection_from_pool)
) -> FeatureCollection:
    return await NeighborhoodService.get_neighborhood(conn, lat, lon)