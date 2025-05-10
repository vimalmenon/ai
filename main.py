from logging import INFO, basicConfig, getLogger

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai.api import (
    router_contact,
    router_rest,
    router_s3,
    router_workflow,
    router_workflow_execute,
    router_workflow_history,
    router_workflow_node,
)
from ai.config.env import env

logger = getLogger(__name__)
basicConfig(
    filename="myapp.log", level=INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger.info("Starting the application...")


app = FastAPI(debug=env.debug)

app.include_router(
    router_contact,
    prefix="/contact",
)
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
    router_workflow_history,
    prefix="/workflow/history",
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
