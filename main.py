from json import JSONDecodeError, dumps, loads
from logging import INFO, basicConfig, getLogger

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from humps import decamelize

from ai.apis import (
    router_blog,
    router_llm_data,
    router_rest,
    router_s3,
    router_workflow,
    router_workflow_execute,
    router_workflow_node,
)
from ai.config.env import env

logger = getLogger(__name__)
basicConfig(
    filename="myapp.log", level=INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger.info("Starting the application...")


app = FastAPI(debug=env.debug)


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
