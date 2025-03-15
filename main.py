import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai.api import (
    router_agent,
    router_contact,
    router_rest,
    router_s3,
    router_workflows,
)
from ai.config.env import env

app = FastAPI(debug=env.debug)

app.include_router(
    router_contact,
    prefix="/contact",
)
app.include_router(
    router_workflows,
    prefix="/workflows",
)

app.include_router(
    router_s3,
    prefix="/s3",
)

app.include_router(
    router_agent,
    prefix="/agent",
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


def run():
    uvicorn.run("main:app", host="0.0.0.0", port=env.port, reload=True)
