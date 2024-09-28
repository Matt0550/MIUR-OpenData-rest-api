from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from dotenv import load_dotenv
load_dotenv()

from app.api.main import api_router
from app.core.config import settings
from app.models import CustomResponse


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    default_response_class=CustomResponse,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Handle 500 errors
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(content={"details": "Internal server error", "status": "error", "code": 500}, status_code=500)

# Handle the 404 error. Use HTTP_exception_handler to handle the error
@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(content={"details": "Not found", "status": "error", "code": exc.status_code}, status_code=exc.status_code)
    elif exc.status_code == 405:
        return JSONResponse(content={"details": "Method not allowed", "status": "error", "code": exc.status_code}, status_code=exc.status_code)
    else:
        # Just use FastAPI's built-in handler for other errors
        return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    print(exc.errors())

    if exc.errors()[0]["type"] == "value_error.any_str.max_length":
        limit = str(exc.errors()[0]["ctx"]["limit_value"])
        return JSONResponse(content={"details": "The value entered is too long. Max length is " + limit, "status": "error", "code": status_code}, status_code=status_code)
    elif exc.errors()[0]["type"] == "value_error.missing":
        missing = []
        for error in exc.errors():
            try:
                missing.append(error["loc"][1])
            except:
                missing.append(error["loc"][0])

        return JSONResponse(content={"details": "One or more fields are missing: " + str(missing), "status": "error", "code": status_code}, status_code=status_code)
    else:
        return JSONResponse(content={"details": exc.errors()[0]["msg"], "status": "error", "code": status_code}, status_code=status_code)

@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    print(exc.errors())

    if exc.errors()[0]["type"] == "value_error.any_str.max_length":
        limit = str(exc.errors()[0]["ctx"]["limit_value"])
        return JSONResponse(content={"details": "The value entered is too long. Max length is " + limit, "status": "error", "code": status_code}, status_code=status_code)
    elif exc.errors()[0]["type"] == "value_error.missing":
        missing = []
        for error in exc.errors():
            try:
                missing.append(error["loc"][1])
            except:
                missing.append(error["loc"][0])

        return JSONResponse(content={"details": "One or more fields are missing: " + str(missing), "status": "error", "code": status_code}, status_code=status_code)
    else:
        return JSONResponse(content={"details": exc.errors()[0]["msg"], "status": "error", "code": status_code}, status_code=status_code)

@app.exception_handler(HTTPException)
async def validation_exception_handler(request: Request, exc: HTTPException):
    print(exc) # 403: The user doesn't have enough privileges

    return JSONResponse(content={"details": exc.detail, "status": "error", "code": exc.status_code}, status_code=exc.status_code)


app.include_router(api_router, prefix=settings.API_V1_STR)