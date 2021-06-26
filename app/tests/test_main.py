from fastapi import FastAPI
from fastapi.testclient import TestClient
from loguru import logger
import pytest
from _pytest.monkeypatch import MonkeyPatch
from starlette.config import Config

from app.exceptions.exceptions import DBConnectionError, DBDisconnectError


def test_startup(app: FastAPI, monkeypatch: MonkeyPatch):
    monkeypatch.setenv("DB_HOST", "foobar") #TODO this test is invalid
    try:
        with TestClient(app) as client:
            pass
    except Exception as e:
        assert type(e) == DBConnectionError

# @pytest.mark.asyncio
# async def test_shutdown(app: FastAPI, monkeypatch: MonkeyPatch):
#     try:
#         with TestClient(app) as client:
#             import pdb; pdb.set_trace()
#             # monkeypatch.delattr("asyncpg.pool.Pool")
#             await app.state.pool.close()
#     except Exception as e:
#         assert type(e) == DBConnectionError
