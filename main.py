import uvicorn
from fastapi import FastAPI

from ai.api import router_contact, router_llm, router_rest, router_workflow
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
    router_llm,
    prefix="/llm",
)

app.include_router(
    router_rest,
)


def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
