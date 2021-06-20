from typing import Any, Dict, List

from asyncpg.connection import Connection
import geojson
from loguru import logger
import numpy as np
import psycopg2

from model.feature import FeatureCollection
from queries import queries

class GeoJSONFormatter:
    def __init__(self, data: Dict[str, Any]):
        self.raw_data = self.processed_data = data
        self.right_hand_rule()
        self.round_decimal(6)

    def right_hand_rule(self):
        """
        Section 3.1.6 https://datatracker.ietf.org/doc/html/rfc7946
        
        A linear ring MUST follow the right-hand rule with respect to the
        area it bounds, i.e., exterior rings are counterclockwise, and
        holes are clockwise.
        """
        data = self.processed_data['features'][0]['geometry']['coordinates'][0]
        data = data[::-1]
        self.processed_data['features'][0]['geometry']['coordinates'][0] = data

    def round_decimal(self, n: int = 0):
        data = self.processed_data['features'][0]['geometry']['coordinates'][0]
        arr = np.array(data)
        data = arr.round(n).tolist()
        self.processed_data['features'][0]['geometry']['coordinates'][0] = data
    
    def get_processed_data(self) -> Dict[str, Any]:
        return self.processed_data


class NeighborhoodService:
    @staticmethod
    @logger.catch
    async def get_neighborhood(conn: Connection, lat: float, lon: float) -> Dict[str, Any]:
        # TODO: try / catch
        ret: List = await queries.get_neighborhood_from_coordinate_as_geojson(conn, lat=lat, lon=lon)
        
        if len(ret) > 0:
            formatter = GeoJSONFormatter(geojson.loads(ret[0]['json_build_object']))
            return formatter.get_processed_data()