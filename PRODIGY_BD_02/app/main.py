from fastapi import FastAPI
from app.api.user_routes import router as user_router
from fastapi.responses import HTMLResponse


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
        content=response_format(exc.status_code, exc.detail["message"], exc.detail.get("data"))
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
        content=response_format(422, "Validation error", exc.errors())
    )

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Users API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                padding: 40px;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 8px;
                max-width: 600px;
                margin: auto;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
            }
            a {
                display: block;
                margin-top: 10px;
                font-size: 18px;
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Bienvenue sur l'API Users</h1>
            <p>Accédez à la documentation :</p>

            <a href="/docs">📘 Swagger UI</a>
            <a href="/redoc">📕 ReDoc</a>
        </div>
    </body>
    </html>
    """
