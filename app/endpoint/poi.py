from asyncpg.connection import Connection
from asyncpg.exceptions import UndefinedTableError
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from jwt.exceptions import ExpiredSignatureError, DecodeError
from loguru import logger

from app.db.database import _get_connection_from_pool
from app.exceptions.exceptions import TokenNotFoundError, LatLonError
from app.model.feature import FeatureCollection
from app.service.poi_service import PoiService
from app.service.token_service import TokenService

poi_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@poi_router.get("/", response_model=FeatureCollection, response_model_exclude_unset=True)
async def poi(
        request: Request,
        lat: float,
        lon: float,
        apikey: str,
        n: int = 10,
        conn: Connection = Depends(_get_connection_from_pool)
) -> FeatureCollection:
    assert 0 <= n < 1000
    # TODO create exception

    try:
        decoded = await TokenService.verify_token(conn, apikey)
        if 'expired' in decoded and decoded['expired'] == True:
            raise ExpiredSignatureError
        del decoded
        return await PoiService.get_k_nearest_neighbors(conn, lat, lon, k=n)
    except ExpiredSignatureError as e:
        logger.info(e)
        payload = {
            "message": "Token has expired. Please get a new API Key 🥲",
            "apikey": apikey,
            'request': request
        }
        return templates.TemplateResponse("request_token.html", payload)
    except TokenNotFoundError as e:
        logger.info(e)
        payload = {"message": "Token not found, please get a new API Key 🥲", "apikey": apikey, 'request': request}
        return templates.TemplateResponse("request_token.html", payload)
    except LatLonError as e:
        # bad input (lat lon)
        logger.info(e)
        return JSONResponse(status_code=400, content={"message": "Bad Request"})
    except DecodeError as e:
        logger.info(e)
    except UndefinedTableError as e:
        logger.info(e)
        raise e
    except Exception as e:
        raise e
