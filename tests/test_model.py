import pytest

from app.model.feature import Feature, FeatureCollection
from app.model.geometry import Polygon


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
    assert len(feature_collection) == len(geojson_feature_collection['features'])
    for f in feature_collection:
        assert type(f) == Feature
    assert type(feature_collection[0]) == Feature
    assert fdict['features'][0]['geometry']['coordinates'] == (-71.073283, 42.417500)
    # assert feature_collection[0].dict()['geometry']['coordinates'] == (-71.073283, 42.417500)


def test_polygon():
    coordinates = [
        [
            [
                151.215291,
                -33.87285
            ],
            [
                151.215317,
                -33.872384
            ],
            [
                151.214834,
                -33.873204
            ],
            [
                151.215291,
                -33.87285
            ]
        ]
    ]
    bad_coordinates = coordinates[0]
    bad_coordinates = bad_coordinates[:2] + bad_coordinates[-1:]
    geojson_polygon = {
        "coordinates": [bad_coordinates],
        "type": "Polygon"
    }
    with pytest.raises(ValueError) as excinfo:
        polygon = Polygon.parse_obj(geojson_polygon)

    assert "All linear rings must have four or more coordinates" in str(excinfo.value)

    bad_coordinates = coordinates[0]
    bad_coordinates[-1] = bad_coordinates[-2]
    geojson_polygon['coordinates'] = [bad_coordinates]

    with pytest.raises(ValueError) as excinfo:
        polygon = Polygon.parse_obj(geojson_polygon)

    assert "All linear rings have the same start and end coordinates" in str(excinfo.value)
