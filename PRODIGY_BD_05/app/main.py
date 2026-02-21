from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from app.api.router import router

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import response_format


app = FastAPI(title="Hotel Booking API")

app.include_router(router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):  
    """
    Custom HTTP exception handler.

    This function is called whenever a HTTP exception is raised.
    It will return a standardized JSONResponse with the status code, message and data from the exception.
    If the exception detail is a dictionary, it will use the keys "message" and "data" to format the response.
    Otherwise, it will use the exception detail as the message and None as the data.

    :param request: The current request
    :param exc: The exception that was raised
    :return: A standardized JSONResponse with the exception details
    """
    if isinstance(exc.detail, dict):
        # Cas standard (TON format)
        return JSONResponse(
            status_code=exc.status_code,
            content=response_format(
                exc.status_code,
                exc.detail.get("message", "Error"),
                exc.detail.get("data"),
            ),
        )

    # Cas FastAPI / HTTPBearer / erreurs natives
    return JSONResponse(
        status_code=exc.status_code,
        content=response_format(
            exc.status_code,
            exc.detail,  # ex: "Not authenticated"
            None,
        ),
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
        content=response_format(422, "Validation error", jsonable_encoder(exc.errors())),
    )