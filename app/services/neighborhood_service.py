import json
from os import stat
from typing import Any, Dict, Tuple

import numpy as np
import psycopg2

GeoJSON = Dict[str, Any]
class GeoJSONFormatter:
    def __init__(self, data: GeoJSON):
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
    
    def get_processed_data(self):
        return self.processed_data


class NeighborhoodService:
    @staticmethod
    def get_neighborhood(db_url: str, lat: float, lon: float) -> GeoJSON:
        # return GeoJson
        sql = """
            WITH neighborhood AS (
                SELECT neighborhood, ST_Transform(geometry, 4326) AS geometry
                FROM nsw_neighborhood
                WHERE ST_Contains(
                    geometry, 
                    ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 8058)
                )
            )
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(ST_AsGeoJSON(neighborhood.*)::json)
            )
            FROM neighborhood
        """

        # return neighborhood and geometry separately
        # sql = """
        #     SELECT neighborhood
        #         , ST_AsGeoJSON(ST_Transform(geometry, 4326)) AS geometry
        #     FROM nsw_neighborhood
        #     WHERE ST_Contains(
        #         geometry, 
        #         ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 8058)
        #     )
        # """
        
        # TODO: try / catch
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute(sql, (lon, lat))

        if cur.rowcount > 0:
            ret = cur.fetchone()
            geojs = GeoJSONFormatter(ret[0])

            return geojs.get_processed_data()