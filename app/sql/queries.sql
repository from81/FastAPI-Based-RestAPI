-- name: get-neighborhood-from-coordinate-as-geojson
-- Given a coordinate, return neighborhood GeoJSON format
WITH neighborhood AS (
    SELECT neighborhood, ST_Transform(geometry, 4326) AS geometry
    FROM nsw_neighborhood
    WHERE ST_Contains(
        geometry, 
        ST_Transform(
            ST_SetSRID(
                ST_MakePoint(:lon, :lat), 
                4326), 
            8058)
    )
)
SELECT json_build_object(
    'type', 
    'FeatureCollection',
    'features', 
    json_agg(ST_AsGeoJSON(neighborhood.*)::json)
)
FROM neighborhood;

-- name: get-neighborhood-from-coordinate
-- Given a coordinate, return neighborhood and geometry
SELECT neighborhood, ST_AsGeoJSON(ST_Transform(geometry, 4326)) AS geometry
FROM nsw_neighborhood
WHERE ST_Contains(
    geometry, 
    ST_Transform(ST_SetSRID(ST_MakePoint(:lon, :lat), 4326), 8058)
);