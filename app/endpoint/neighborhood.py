from asyncpg.connection import Connection
from fastapi import APIRouter, Depends

from app.database import _get_connection_from_pool
from app.model.feature import FeatureCollection
from app.service.neighborhood_service import NeighborhoodService
from app.service.token_service import TokenService

neighborhood_router = APIRouter()

@neighborhood_router.get("/", response_model=FeatureCollection, response_model_exclude_unset=True)
async def neighborhood(
    lat: float, lon: float, apikey: str, conn: Connection = Depends(_get_connection_from_pool)
) -> FeatureCollection:
    exists = await TokenService.verify_token(conn, apikey)
    if exists:
        return await NeighborhoodService.get_neighborhood(conn, lat, lon)