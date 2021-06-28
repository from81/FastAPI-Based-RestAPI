import uuid
from asyncpg.pool import Pool
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.service.neighborhood_service import NeighborhoodService
from app.service.token_service import TokenService
from app.exceptions.exceptions import LatLonError, TokenNotFoundError


def test_home(app: FastAPI):
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_app(app: FastAPI):
    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


def test_client(app: FastAPI):
    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


def test_create_token_json(app: FastAPI):
    with TestClient(app) as client:
        response = client.post("/token",
                               headers={
                                   "Content-Type": "application/json"
                               },
                               json={"email": "test@foo.bar.com"}
                               )
    assert response.status_code == 200
    assert response.json()["message"] == "OK"


def test_create_apikey_get(app: FastAPI):
    with TestClient(app) as client:
        response = client.get("/apikey")
    assert response.status_code == 200
    assert response.template.name == 'request_token.html'


def test_create_apikey_post(app: FastAPI):
    # Generate a random UUID
    email = f"{uuid.uuid1()}@gmail.com"

    with TestClient(app) as client:
        response = client.post("/apikey", data={"email": email})
    assert response.status_code == 200
    assert response.context['message'] == "OK"
    assert response.template.name == 'request_token.html'


def test_create_apikey_post_noemail(app: FastAPI):
    with TestClient(app) as client:
        response = client.post("/apikey", data={"email": None})
    assert response.status_code == 200
    assert response.template.name == 'request_token.html'
    assert response.context['message'] == "Email invalid or not found."


def test_get_neighborhood(app: FastAPI, valid_apikey: str):
    with TestClient(app) as client:
        response = client.get(
            "/neighborhood",
            params={
                "lat": -33.8657512,
                "lon": 151.2030053,
                "apikey": valid_apikey
            }
        )
    js = response.json()
    assert response.status_code == 200
    assert js["type"] == "FeatureCollection"
    assert js["features"][0]["properties"]["neighborhood"] == "SYDNEY"


def test_get_neighborhood_expired_apikey(app: FastAPI, expired_apikey: str):
    with TestClient(app) as client:
        response = client.get(
            "/neighborhood",
            params={
                "lat": -33.8657512,
                "lon": 151.2030053,
                "apikey": expired_apikey
            }
        )
        assert response.template.name == 'request_token.html'
        assert response.context['message'] == "Token has expired. Please get a new API Key 🥲"
        assert response.context['apikey'] == expired_apikey


# TODO obstacle: TokenNotFoundError raised, but not detected by pytest?
# @pytest.mark.asyncio
# async def test_verify_invalid_token(pool: Pool):
#     invalid_apikey = "invalid_key"
#     async with pool.acquire() as conn:
#         with pytest.raises(TokenNotFoundError) as excinfo:
#             decoded = await TokenService.verify_token(conn, invalid_apikey)
#
#     assert 'Token not found' in str(excinfo.value)

# do this after testing token_service.verify_token
# def test_get_neighborhood_invalid_apikey(app: FastAPI):
#     invalid_apikey = "invalid_key"
#     with TestClient(app) as client:
#         response = client.get(
#             "/neighborhood",
#             params={
#                 "lat": -33.8657512,
#                 "lon": 151.2030053,
#                 "apikey": invalid_apikey
#             }
#         )
#         assert response.template.name == 'request_token.html'
#         assert response.context['message'] == "Token not found, please get a new API Key 🥲"
#         assert response.context['apikey'] == invalid_apikey


# @pytest.mark.asyncio
# async def test_get_neighborhood_invalid_coordinate(initialized_app: FastAPI, pool: Pool):
#     #TODO obstacle: LatLonError raised, but not detected by pytest
#     lat, lon = 0, 0
#     with pytest.raises(LatLonError) as excinfo:
#         async with pool.acquire() as conn:
#             ret: Dict = await NeighborhoodService.get_neighborhood(conn, lat, lon)
#
#     assert 'Invalid coordinates' in str(excinfo.value)


def test_get_k_poi(app: FastAPI, valid_apikey: str):
    k = 5
    with TestClient(app) as client:
        response = client.get(
            "/poi",
            params={
                "lat": -33.8657512,
                "lon": 151.2030053,
                "apikey": valid_apikey,
                "n": k
            }
        )
    js = response.json()
    assert response.status_code == 200
    assert js["type"] == "FeatureCollection"
    assert len(js["features"]) == k
    assert js["features"][0]["properties"].keys() == {"fclass", "name", "osm_id", "distance"}
    assert js["features"][0]["geometry"]["type"] == "Point"


def test_get_k_poi_expired_apikey(app: FastAPI, expired_apikey: str):
    k = 5
    with TestClient(app) as client:
        response = client.get(
            "/poi",
            params={
                "lat": -33.8657512,
                "lon": 151.2030053,
                "apikey": expired_apikey,
                "n": k
            }
        )
    assert response.template.name == 'request_token.html'
    assert response.context['message'] == "Token has expired. Please get a new API Key 🥲"
    assert response.context['apikey'] == expired_apikey
