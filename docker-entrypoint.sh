#!/usr/bin/bash
set -e

service postgresql start
gdalinfo --version
psql -U $POSTGRES_USER -c "CREATE DATABASE ${POSTGRES_DB};"
psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/ddl.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -c "ALTER USER postgres WITH password 'postgres';"
python /docker-entrypoint-initdb.d/insert_data.py
exec "$@"