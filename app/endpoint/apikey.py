import asyncio

from asyncpg.connection import Connection
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

from database import _get_connection_from_pool
from service.apikey_service import APIKeyService

apikey_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@apikey_router.get("", response_class=HTMLResponse)
@apikey_router.post("")
async def token(request: Request, conn: Connection = Depends(_get_connection_from_pool)):
    if request.method == "GET":
        return templates.TemplateResponse("request_token.html", {"request": request})
    elif request.method == "POST":
        form = await request.form()
        email = form['email']
        
        try:
            logger.info(f"Issuing token for {email}")
            token = APIKeyService.issue_token(conn, email)
            await APIKeyService.register_token(conn, email, token)
            payload = {"token": token, "request": request}
            return templates.TemplateResponse("request_token.html", payload)
        except Exception as e:
            logger.warning(e)