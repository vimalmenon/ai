import os

from pydantic import BaseModel


class Env(BaseModel):
    temperature: float = float(os.getenv("TEMPERATURE", 0.0))
    notes_path: str = f"{os.getcwd()}/ai/data/notes/data.txt"


env = Env()
