from asyncpg.pool import Pool
from fastapi import FastAPI
from fastapi.testclient import TestClient
from loguru import logger
import pytest
from tests.conftest import app
from _pytest.monkeypatch import MonkeyPatch
from starlette.config import Config

from app.exceptions.exceptions import DBConnectionError, DBDisconnectError


def test_startup(app: FastAPI, monkeypatch: MonkeyPatch):
    monkeypatch.setattr("app.main.DB_URL", f"postgresql://test@foobar/postgres", raising=True)

    with pytest.raises(DBConnectionError) as excinfo:
        with TestClient(app) as client:
            pass
    assert 'Failed to connect to the database' in str(excinfo.value)

# def test_shutdown(app: FastAPI, monkeypatch: MonkeyPatch):
#
#     with pytest.raises(DBDisconnectError) as excinfo:
#         with TestClient(app) as client:
#             # import pdb; pdb.set_trace()
#             # monkeypatch.delattr("asyncpg.pool.Pool", raising=True)
#             monkeypatch.delattr("app", "state", raising=True)
#
#     assert 'Failed to disconnect from the database' in str(excinfo.value), str(excinfo.value)
