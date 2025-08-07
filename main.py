import sys
import time
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from json import JSONDecodeError, dumps, loads
from logging import DEBUG, FileHandler, StreamHandler, basicConfig, getLogger

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
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

# Configure logging to both file and console
basicConfig(
    level=DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        StreamHandler(sys.stdout),  # Console output
        FileHandler("myapp.log"),  # File output
    ],
)

logger.info("Starting the application...")

env = Env()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    logger.info("Application startup completed")
    yield
    # Shutdown
    logger.info("Application shutdown completed")


app = FastAPI(
    debug=env.debug,
    title="AI API",
    description="AI Agent API for workflow management and LLM interactions",
    version=env.version if hasattr(env, "version") else "0.0.19",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors."""
    error_details = []
    for error in exc.errors():
        # Maintain backward compatibility with original structure
        error_detail = {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
            # Add improved structure as well
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
        }
        error_details.append(error_detail)

    logger.error(f"Request validation error on {request.url}: {error_details}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": error_details,
        },
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.error(f"Pydantic validation error on {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Data validation failed",
            "details": exc.errors(),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.error(f"HTTP exception on {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    logger.error(f"Unexpected error on {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred" if not env.debug else str(exc),
        },
    )


@app.middleware("http")
async def convert_camel_to_snake(request: Request, call_next: Callable) -> Response:
    """Convert camelCase request body to snake_case."""
    if request.method in ("POST", "PUT", "PATCH") and request.headers.get(
        "content-type", ""
    ).startswith("application/json"):
        body = await request.body()
        if body:
            try:
                json_data = loads(body)
                snake_data = decamelize(json_data)

                # Create a new request with modified body
                async def receive():
                    return {
                        "type": "http.request",
                        "body": dumps(snake_data).encode(),
                        "more_body": False,
                    }

                # Override the receive callable
                request._receive = receive

            except (JSONDecodeError, Exception) as e:
                logger.warning(f"Failed to convert camelCase to snake_case: {e}")

    response = await call_next(request)
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Response:
    """Log request details and response time."""
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url}")

    response = await call_next(request)

    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")

    return response


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "message": "AI Agent API",
        "version": getattr(env, "version", "0.0.19"),
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": getattr(env, "version", "0.0.19"),
        "environment": getattr(env, "env", "development"),
        "timestamp": time.time(),
    }


# Include routers
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

# Configure CORS
allowed_origins = ["http://localhost:3000"]
if hasattr(env, "allowed_origins") and env.allowed_origins:
    allowed_origins = env.allowed_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)


def run() -> None:
    """Run the FastAPI application."""
    host = getattr(env, "host", "0.0.0.0")
    port = getattr(env, "port", 8000)
    reload = getattr(env, "debug", False)

    logger.info(f"Starting server on {host}:{port} with reload={reload}")
    uvicorn.run("main:app", host=host, port=port, reload=reload)
