from fastapi import FastAPI
from fastapi.testclient import TestClient
from loguru import logger
import pytest
from tests.conftest import app
from _pytest.monkeypatch import MonkeyPatch
from starlette.config import Config

from app.exceptions.exceptions import DBConnectionError, DBDisconnectError


def test_startup(app: FastAPI, config: Config, monkeypatch: MonkeyPatch):
    # TODO this test is invalid
    # import pdb; pdb.set_trace()

    # monkeypatch.setenv("DB_HOST", "foobar")
    monkeypatch.setattr("app.main.DB_URL", f"postgresql://test@foobar/postgres", raising=True)

    # config.__dict__['file_values']['DB_HOST'] = 'foobar'
    # del config.__dict__['file_values']['DB_HOST']

    with pytest.raises(DBConnectionError) as excinfo:
        with TestClient(app) as client:
            pass
    assert 'Failed to connect to the database' in str(excinfo.value)

# @pytest.mark.asyncio
# async def test_shutdown(app: FastAPI, monkeypatch: MonkeyPatch):
#     try:
#         with TestClient(app) as client:
#             import pdb; pdb.set_trace()
#             # monkeypatch.delattr("asyncpg.pool.Pool")
#             await app.state.pool.close()
#     except Exception as e:
#         assert type(e) == DBConnectionError
