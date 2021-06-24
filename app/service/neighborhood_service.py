from typing import Any, Dict, List

from asyncpg.connection import Connection
import geojson
from loguru import logger

from app.db.sql_queries import queries
from app.utils.geojson_formatter import GeoJSONFormatter

class NeighborhoodService:
    @staticmethod
    @logger.catch
    async def get_neighborhood(conn: Connection, lat: float, lon: float) -> Dict[str, Any]:
        # TODO: try / catch
        ret: List = await queries.get_neighborhood_from_coordinate_as_geojson(conn, lat=lat, lon=lon)
        
        if len(ret) > 0:
            formatter = GeoJSONFormatter(geojson.loads(ret[0]['json_build_object']))
            return formatter.get_processed_data()
        else:
            raise LatLonError(lat, lon)