import uvicorn
from fastapi import FastAPI

from ai.api import router_contact

app = FastAPI()


app.include_router(
    router_contact,
    prefix="/contact",
)


def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
