from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_home(app: FastAPI):
    client = TestClient(app)
    response = client.get("/test")
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


def test_create_apikey(app: FastAPI):
    with TestClient(app) as client:
        response = client.get("/apikey")
    assert response.status_code == 200
    assert response.template.name == 'request_token.html'


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
