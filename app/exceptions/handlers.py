from http import HTTPStatus
from json.decoder import JSONDecodeError

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.exceptions.exceptions import NotFoundException


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request, exc):
        return JSONResponse(
            content=jsonable_encoder({"detail": exc.errors()}),
            status_code=HTTPStatus.BAD_REQUEST
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request, exc):
        return await request_validation_exception_handler(request, exc)

    @app.exception_handler(Exception)
    async def internal_server_exception_handler(request, exc):
        return JSONResponse(
            content=jsonable_encoder({"detail": {"msg": str(exc)}}),
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request, exc):
        return JSONResponse(
            content=jsonable_encoder({"detail": {"msg": str(exc)}}),
            status_code=HTTPStatus.NOT_FOUND
        )

    @app.exception_handler(JSONDecodeError)
    async def json_decode_exception_handler(request, exc):
        return JSONResponse(
            content=jsonable_encoder({"detail": {"msg": str(exc)}}),
            status_code=HTTPStatus.BAD_REQUEST
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            content=jsonable_encoder({
                "detail": {
                    "status": exc.status_code,
                    "msg": exc.detail,
                    "headers": exc.headers
                },
            }),
            status_code=exc.status_code
        )
