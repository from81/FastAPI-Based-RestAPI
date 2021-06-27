import asyncio

from asyncpg.connection import Connection
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

from app.db.database import _get_connection_from_pool
from app.service.token_service import TokenService

apikey_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@apikey_router.get("", response_class=HTMLResponse)
@apikey_router.post("")
@logger.catch
async def apikey(request: Request, conn: Connection = Depends(_get_connection_from_pool)):
    if request.method == "GET":
        return templates.TemplateResponse("request_token.html", {"request": request})
    elif request.method == "POST":

        form = await request.form()
        try:
            email = form['email']
        except KeyError as e:
            logger.info("Email not found in form data.")
            return templates.TemplateResponse(
                "request_token.html",
                {"message": "Email invalid or not found.", "request": request}
            )

        logger.info(f"Issuing token for {email}")
        token = TokenService.issue_token(conn, email)
        await TokenService.register_token(conn, email, token)
        payload = {"token": token, "request": request, "message": "OK"}
        return templates.TemplateResponse("request_token.html", payload)
