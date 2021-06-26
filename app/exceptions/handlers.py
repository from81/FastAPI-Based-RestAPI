from fastapi import Request
from fastapi.responses import JSONResponse, HTMLResponse

from app.exceptions.exceptions import DBConnectionError, DBDisconnectError

async def handler_DBConnectionError(request: Request, exc: DBConnectionError):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)}
    )
async def handler_DBDisconnectError(request: Request, exc: DBDisconnectError):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)}
    )

# HTML_404_PAGE = ...
# HTML_500_PAGE = ...


# async def not_found(request, exc):
#     return HTMLResponse(content=HTML_404_PAGE, status_code=exc.status_code)

# async def server_error(request, exc):
#     return HTMLResponse(content=HTML_500_PAGE, status_code=exc.status_code)

# async def http_exception(request, exc):
#     return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

exception_handlers = {
    DBConnectionError: handler_DBConnectionError,
    DBDisconnectError: handler_DBDisconnectError
    # 404: not_found,
    # 500: server_error,
}
