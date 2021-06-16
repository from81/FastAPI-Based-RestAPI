SELECT neighborhood, geometry
FROM nsw_neighborhood
WHERE ST_Contains(geometry, ST_MakePoint());
-- ST_Contains(a,b) true if a contains b
-- ST_MakePoint(X,Y) X is longitude and Y is latitude

-- return neighborhood and geometry separately
SELECT neighborhood
    , ST_AsGeoJSON(ST_Transform(geometry, 4326)) AS geometry
FROM nsw_neighborhood
WHERE ST_Contains(
    geometry, 
    ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 8058)
);