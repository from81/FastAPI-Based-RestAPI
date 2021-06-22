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

@pytest.fixture
def client() -> TestClient:
    from app.main import app  # local import for testing purpose
    return TestClient(app)

@pytest.fixture
def config():
    from app import config 
    return config

@pytest.fixture
def expired_apikey():
    from app.config import JWT_PRIVATE_KEY, ALGORITHM
    payload = {
        'iss': "test@foobar.com",
        'exp': datetime.utcnow()
    }
    encoded = jwt.encode(payload, JWT_PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded

@pytest.fixture
def valid_apikey():
    from app.config import JWT_PRIVATE_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
    payload = {
        'iss': "test@foobar.com",
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    encoded = jwt.encode(payload, JWT_PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded