from datetime import datetime
import sys

sys.path.append('../app/')

from asgi_lifespan import LifespanManager
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
import pytest


@pytest.fixture
def app() -> FastAPI:
    from app.main import app  # local import for testing purpose
    return app


@pytest.fixture
def config():
    from app.config import config
    return config


@pytest.fixture(scope='session')
def expired_apikey():
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0ZXN0QGZvb2Jhci5jb20iLCJleHAiOjE2MjQ0Mzg1Njh9.hk4NMXcMzw5uVzwg1t3fOsfsuMby1qBzK5m5gsk8Gj4'
    return expired_token


@pytest.fixture
def valid_apikey(scope='session'):
    from app.config import TEST_API_KEY
    return str(TEST_API_KEY)


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture
def pool(initialized_app: FastAPI) -> Pool:
    return initialized_app.state.pool


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
            app=initialized_app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
    ) as client:
        yield client
