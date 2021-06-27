from typing import Any, Dict, List

from asyncpg.connection import Connection
import geojson
from loguru import logger

from app.db.sql_queries import queries
from app.utils.geojson_formatter import GeoJSONFormatter
from app.exceptions.exceptions import LatLonError


class PoiService:
    @staticmethod
    @logger.catch
    async def get_k_nearest_neighbors(conn: Connection, lat: float, lon: float, k: int) -> Dict[str, Any]:
        ret: List = await queries.get_k_poi_as_geojson(conn, lat=lat, lon=lon, k=k)
        geojson_data = geojson.loads(ret[0]['json_build_object'])

        if geojson_data['features'] and len(geojson_data['features']) > 0:
            formatter = GeoJSONFormatter(geojson_data, right_hand_rule=False)
            return formatter.get_processed_data()
        else:
            raise LatLonError(lat, lon)
