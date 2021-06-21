from asyncpg.connection import Connection
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from jwt.exceptions import ExpiredSignatureError, DecodeError
from loguru import logger

from app.database import _get_connection_from_pool
from app.exceptions.exceptions import TokenNotFoundError, LatLonError
from app.model.feature import FeatureCollection
from app.service.neighborhood_service import NeighborhoodService
from app.service.token_service import TokenService

neighborhood_router = APIRouter()

@neighborhood_router.get("/", response_model=FeatureCollection, response_model_exclude_unset=True)
async def neighborhood(
    lat: float, lon: float, apikey: str, conn: Connection = Depends(_get_connection_from_pool)
) -> FeatureCollection:
    try:
        decoded = await TokenService.verify_token(conn, apikey)
        return await NeighborhoodService.get_neighborhood(conn, lat, lon)
    except TokenNotFoundError as e:
        # token not found exception
        logger.info("Token not found")
        return JSONResponse(status_code=401, content={"message": "Authorization Required"})
    except ExpiredSignatureError as e:
        #TODO redirect user to "token/" for updating apikey
        pass
    except DecodeError as e:
        pass
    except LatLonError as e:
        # bad input (lat lon)
        logger.info(e)
        return JSONResponse(status_code=400, content={"message": "Bad Request"})