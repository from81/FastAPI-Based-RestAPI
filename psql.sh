DB_USER=$(jq -r '.username' $1)
DB_PW=$(jq -r '.password' $1)
DB_HOST=$(jq -r '.host' $1)
DB_PORT=$(jq -r '.port' $1)
DB_DB=$(jq -r '.database' $1)

PGPASSWORD=$DB_PW psql -h $DB_HOST -U $DB_USER -d $DB_DB
