from datetime import datetime
import sys

sys.path.append('../')

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
import jwt


@pytest.fixture
def app() -> FastAPI:
    from app.main import app  # local import for testing purpose
    return app


# @pytest.fixture
# def client(app: FastAPI) -> TestClient:
#     client = TestClient(app)
#     yield client

@pytest.fixture
def config():
    from app.config import config
    return config


@pytest.fixture
def expired_apikey():
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0ZXN0QGZvb2Jhci5jb20iLCJleHAiOjE2MjQ0Mzg1Njh9.hk4NMXcMzw5uVzwg1t3fOsfsuMby1qBzK5m5gsk8Gj4'
    return expired_token


@pytest.fixture
def valid_apikey():
    from app.config import TEST_API_KEY
    return str(TEST_API_KEY)
