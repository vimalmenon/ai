from json import JSONDecodeError, dumps, loads
from logging import DEBUG, basicConfig, getLogger

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from humps import decamelize
from pydantic import ValidationError

from ai.apis import (
    router_ai_messages,
    router_blog,
    router_links,
    router_llm_data,
    router_rest,
    router_s3,
    router_workflow,
    router_workflow_execute,
    router_workflow_node,
)
from ai.config import Env

logger = getLogger(__name__)
basicConfig(
    filename="myapp.log",
    level=DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger.info("Starting the application...")

env = Env()
app = FastAPI(debug=env.debug)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.error(f"Request validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": exc.errors(),
        },
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    logger.error(f"Pydantic validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Data validation failed",
            "details": exc.errors(),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
        },
    )


@app.middleware("http")
async def convert_camel_to_snake(request: Request, call_next):
    if request.method in (
        "POST",
        "PUT",
        "PATCH",
    ) and "application/json" in request.headers.get("content-type", ""):
        body = await request.body()
        if body:
            try:
                json_data = loads(body)
                snake_data = decamelize(json_data)
                # Modify request to use snake_case data
                request._body = dumps(snake_data).encode()
            except JSONDecodeError:
                pass

    response = await call_next(request)
    return response


app.include_router(
    router_workflow,
    prefix="/workflow",
)
app.include_router(
    router_workflow_node,
    prefix="/workflow/node",
)
app.include_router(
    router_workflow_execute,
    prefix="/workflow/execute",
)

app.include_router(
    router_blog,
    prefix="/blog",
)

app.include_router(
    router_llm_data,
    prefix="/llm_data",
)

app.include_router(
    router_s3,
    prefix="/s3",
)

app.include_router(
    router_links,
    prefix="/links",
)

app.include_router(
    router_ai_messages,
    prefix="/ai_messages",
)

app.include_router(
    router_rest,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run() -> None:
    """Run the FastAPI application."""
    uvicorn.run("main:app", host="0.0.0.0", port=env.port, reload=True)
