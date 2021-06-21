import sys
sys.path.append('../')

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

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