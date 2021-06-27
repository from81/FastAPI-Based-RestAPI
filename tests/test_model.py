from app.model.feature import Feature, FeatureCollection


def test_feature():
    geojson_feature = {
        "type": "Feature",
        "properties": {
            "name": "Coors Field",
            "amenity": "Baseball Stadium",
            "popupContent": "This is where the Rockies play!"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-104.99404, 39.75621]
        }
    }
    feature = Feature.parse_obj(geojson_feature)
    fdict = feature.dict(exclude_unset=True)
    assert type(feature) == Feature
    assert fdict['type'] == 'Feature'
    assert fdict.keys() == {'type', 'properties', 'geometry'}
    assert fdict['geometry']['coordinates'] == (-104.99404, 39.75621)


def test_feature_collection():
    geojson_feature_collection = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {
                "capacity": "10",
                "type": "U-Rack",
                "mount": "Surface"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-71.073283, 42.417500]
            }
        }]
    }
    feature_collection = FeatureCollection.parse_obj(geojson_feature_collection)
    fdict = feature_collection.dict(exclude_unset=True)
    assert type(feature_collection) == FeatureCollection
    assert fdict['type'] == 'FeatureCollection'
    assert fdict.keys() == {'type', 'features'}
    assert len(fdict['features']) == len(geojson_feature_collection['features'])
    assert fdict['features'][0]['geometry']['coordinates'] == (-71.073283, 42.417500)
