BEGIN;
    CREATE EXTENSION IF NOT EXISTS postgis;

    CREATE TABLE IF NOT EXISTS nsw_neighborhood (
        neighborhood TEXT
    );
    -- Add a spatial column to the table
    SELECT AddGeometryColumn ('nsw_neighborhood', 'geometry', 8058, 'POLYGON', 2);
    CREATE INDEX idx_nsw_neighborhood_geometry ON nsw_neighborhood USING GIST ("geometry");

    CREATE TABLE IF NOT EXISTS nsw_poi (
        osm_id TEXT,
        code BIGINT,
        fclass TEXT,
        "name" TEXT
    );
    SELECT AddGeometryColumn ('nsw_poi', 'geometry', 8058, 'POLYGON', 2);
    CREATE INDEX idx_nsw_poi_geometry ON nsw_poi USING GIST ("geometry");

    CREATE TABLE IF NOT EXISTS nsw_polygon (
        "name" TEXT
    );
    SELECT AddGeometryColumn ('nsw_polygon', 'geometry', 8058, 'POLYGON', 2);
    CREATE INDEX idx_nsw_polygon_geometry ON nsw_polygon USING GIST ("geometry");

    CREATE TABLE IF NOT EXISTS apikey (
        email TEXT,
        token TEXT,
        PRIMARY KEY(email, token)
    );
COMMIT;
-- ROLLBACK;