import uvicorn
from fastapi import FastAPI

from ai.api import router_contact, router_rest, router_s3, router_workflow
from ai.config.env import env

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
    router_s3,
    prefix="/s3",
)

app.include_router(
    router_rest,
)


def run():
    uvicorn.run("main:app", host="0.0.0.0", port=env.port, reload=True)
