from asyncpg.connection import Connection
from asyncpg.exceptions import UndefinedTableError
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from jwt.exceptions import ExpiredSignatureError, DecodeError
from loguru import logger

from app.database import _get_connection_from_pool
from app.exceptions.exceptions import TokenNotFoundError, LatLonError
from app.model.feature import FeatureCollection
from app.service.neighborhood_service import NeighborhoodService
from app.service.token_service import TokenService

neighborhood_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@neighborhood_router.get("/", response_model=FeatureCollection, response_model_exclude_unset=True)
async def neighborhood(
    request: Request, 
    lat: float, 
    lon: float, 
    apikey: str, 
    conn: Connection = Depends(_get_connection_from_pool)
) -> FeatureCollection:
    # import pdb; pdb.set_trace()
    try:
        decoded = await TokenService.verify_token(conn, apikey)
        del decoded
        return await NeighborhoodService.get_neighborhood(conn, lat, lon)
    except TokenNotFoundError as e:
        # token not found exception
        logger.info("Token not found")
        
        return JSONResponse(status_code=401, content={"message": "Authorization Required"})
    except LatLonError as e:
        # bad input (lat lon)
        logger.info(e)
        return JSONResponse(status_code=400, content={"message": "Bad Request"})
    except ExpiredSignatureError as e:
        #TODO redirect user to "token/" for updating apikey
        logger.info(e)
        payload = {"message": "Token expired, please get a new API Key 🥲", "apikey": apikey}
        return templates.TemplateResponse("request_token.html", payload)
    except DecodeError as e:
        logger.info(e)
    except UndefinedTableError as e:
        logger.info(e)
        raise e
    except Exception as e:
        raise e