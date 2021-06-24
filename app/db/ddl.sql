DROP TABLE IF EXISTS nsw_neighborhood;
DROP TABLE IF EXISTS nsw_poi;
DROP TABLE IF EXISTS nsw_polygon;
DROP TABLE IF EXISTS apikey;

BEGIN;
    CREATE EXTENSION IF NOT EXISTS postgis;

    CREATE TABLE IF NOT EXISTS nsw_neighborhood (
        neighborhood TEXT
    );
    -- Add a spatial column to the table
    SELECT AddGeometryColumn ('nsw_neighborhood', 'geometry', 4326, 'POLYGON', 2);
    CREATE INDEX idx_nsw_neighborhood_geometry ON nsw_neighborhood USING GIST ("geometry");

    CREATE TABLE IF NOT EXISTS nsw_poi (
        osm_id TEXT,
        fclass TEXT,
        "name" TEXT
    );
    SELECT AddGeometryColumn ('nsw_poi', 'geometry', 4326, 'POLYGON', 2);
    CREATE INDEX idx_nsw_poi_geometry ON nsw_poi USING GIST ("geometry");

    CREATE TABLE IF NOT EXISTS nsw_polygon (
        "name" TEXT
    );
    SELECT AddGeometryColumn ('nsw_polygon', 'geometry', 4326, 'POLYGON', 2);
    CREATE INDEX idx_nsw_polygon_geometry ON nsw_polygon USING GIST ("geometry");

    CREATE TABLE IF NOT EXISTS apikey (
        email TEXT,
        token TEXT,
        PRIMARY KEY(email, token)
    );

    INSERT INTO apikey (email, token) VALUES (
        'test@foobar.com',
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0ZXN0QGZvb2Jhci5jb20iLCJleHAiOjIyMjkyMzk3MDR9.34qCT0kVYo58JnwdoQP5nDFksPkVVlKePQaJk4Z5o6g'
        -- valid token
    );

    INSERT INTO apikey (email, token) VALUES (
        'test@foobar.com',
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0ZXN0QGZvb2Jhci5jb20iLCJleHAiOjE2MjQ0Mzg1Njh9.hk4NMXcMzw5uVzwg1t3fOsfsuMby1qBzK5m5gsk8Gj4'
        -- expired token
    );
COMMIT;
-- ROLLBACK;