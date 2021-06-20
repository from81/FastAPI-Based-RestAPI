-- name: get-tables
-- Show tables
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';

-- name: create-apikey-table
-- Create apikey table
CREATE TABLE IF NOT EXISTS apikey (
    email VARCHAR,
    token VARCHAR,
    PRIMARY KEY(email, token)
);

-- name: insert-apikey!
-- Insert apikey
INSERT INTO apikey (email, token) VALUES (:email, :token);

-- name: verify-apikey
-- Verify apikey
SELECT email, token FROM apikey WHERE token = :token;

-- name: delete-apikey!
-- Delete rows with matching email address
DELETE FROM apikey WHERE email = :email;

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