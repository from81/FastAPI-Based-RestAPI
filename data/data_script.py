import os
import sys

import geojson
import geopandas as gpd
# from sqlalchemy import create_engine

sys.path.append("..")
from app.utils.geojson_formatter import GeoJSONFormatter

class GeoData:
    def __init__(self, path: str):
        self.path = path
        self.input_dir, self.input_file = os.path.split(path)
        
        if '/in/' in self.input_dir:
            self.output_dir = self.input_dir.replace('/in/', '/out/')

        self.epsg4326 = gpd.read_file(path).to_crs(epsg=4326)
        self.epsg8058 = self.epsg4326.copy().to_crs(epsg=8058)

    def to_geojson(self):
        geojs = geojson.loads(self.epsg4326.to_json())
        formatter = GeoJSONFormatter(geojs)
        formatted_geojs = formatter.get_processed_data()

        fname, ext = os.path.splitext(self.input_file)
        output_dir = self.output_dir if self.output_dir else self.input_dir
        path = os.path.join(output_dir, fname + '.json')
        
        with open(path, 'w') as f:
            geojson.dump(formatted_geojs, f)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('example: python pipeline.py <path to input file>')
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print('File does not exist')
        sys.exit(1)

    data = GeoData(path)
    data.to_geojson()