import os
import sys

import geopandas as gpd
from sqlalchemy import create_engine

if len(sys.argv) < 2:
    print("python insert_data.py <path to dir>")
    sys.exit(1)

DATA_DIR = sys.argv[1]

try:
    # use unix file socket instead of localhost
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    POSTGRES_DB = os.environ['POSTGRES_DB']
    conn_str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@/{POSTGRES_DB}"
    engine = create_engine(conn_str)

    for file in os.listdir(DATA_DIR):
        name, ext = os.path.splitext(file)
        if ext == '.json':
            print(name)
            df = gpd.read_file(os.path.join(DATA_DIR, file))
            df.to_postgis(name, engine, if_exists='replace')
except Exception as e:
    print(e)
