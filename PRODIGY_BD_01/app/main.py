# app/main.py
from fastapi import FastAPI
from app.api.user_routes import router as user_router

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import response_format


app = FastAPI(title="Users API")

app.include_router(user_router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Custom exception handler for StarletteHTTPException.

    This function will be called whenever a StarletteHTTPException is raised.
    It will return a JSONResponse with the status code, message and data
    from the exception.

    :param request: The current request
    :param exc: The exception that was raised
    :return: A JSONResponse with the exception details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=response_format(exc.status_code, exc.detail['message'], exc.detail.get("data"))
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler for RequestValidationError.

    This function will be called whenever a RequestValidationError is raised.
    It will return a JSONResponse with the status code, message and data
    from the exception.

    :param request: The current request
    :param exc: The exception that was raised
    :return: A JSONResponse with the exception details
    """
    return JSONResponse(
        status_code=422,
        content=response_format(422, "Erreur de validation", exc.errors())
    )

