import asyncio

from asyncpg.connection import Connection
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from loguru import logger

from app.db.database import _get_connection_from_pool
from app.service.token_service import TokenService

token_router = APIRouter()

@token_router.post("", response_class=JSONResponse)
@logger.catch
async def token(request: Request, conn: Connection = Depends(_get_connection_from_pool)):
    try:
        js = await request.json()
        email = js['email']
        logger.info(f"Issuing token for {email}")
        token = TokenService.issue_token(conn, email)
        await TokenService.register_token(conn, email, token)
        return JSONResponse(
            status_code=200, 
            content={"message": "OK", "token": token}
        )
    except Exception as e:
        logger.warning(e)