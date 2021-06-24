import os

import geopandas as gpd
from sqlalchemy import create_engine
DATA_DIR = '/data'

# use unix file socket instead of localhost
engine = create_engine(f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@/{os.environ['POSTGRES_DB']}")

for file in os.listdir(DATA_DIR):
    name, ext = os.path.splitext(file)
    if ext == '.json':
        print(name)
        df = gpd.read_file(os.path.join(DATA_DIR, file))
        df.to_postgis(name, engine, if_exists='replace')

