import json
from typing import Dict, Tuple

from psycopg2.extensions import cursor

Cursor = cursor
Geometry = Dict

class NeighborhoodService:
    @staticmethod
    def get_neighborhood(cur: Cursor, lat: float, lon: float) -> Tuple[str, Geometry]:
        sql = """
            SELECT neighborhood
                , ST_AsGeoJSON(ST_Transform(geometry, 4326)) AS geometry
            FROM nsw_neighborhood
            WHERE ST_Contains(
                geometry, 
                ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 8058)
            )
        """
        #TODO: try / catch
        cur.execute(sql, (lon, lat))

        if cur.rowcount > 0:
            neighborhood, geom = cur.fetchone()
            geom = json.loads(geom)
            return neighborhood, geom