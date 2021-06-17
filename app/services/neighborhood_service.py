import json
from typing import Any, Dict, Tuple

from psycopg2.extensions import cursor

Cursor = cursor
GeoJSON = Dict[str, Any]

def right_hand_rule(data: GeoJSON) -> GeoJSON:
    """
    Section 3.1.6 https://datatracker.ietf.org/doc/html/rfc7946
    
    A linear ring MUST follow the right-hand rule with respect to the
    area it bounds, i.e., exterior rings are counterclockwise, and
    holes are clockwise.
    """

    data['features'][0]['geometry']['coordinates'][0] = data['features'][0]['geometry']['coordinates'][0][::-1]
    return data

class NeighborhoodService:
    @staticmethod
    def get_neighborhood(cur: Cursor, lat: float, lon: float) -> GeoJSON:
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
        cur.execute(sql, (lon, lat))

        if cur.rowcount > 0:
            geojs = cur.fetchone()
            return right_hand_rule(geojs[0])