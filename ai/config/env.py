from pydantic import BaseModel
import os


class Env(BaseModel):
    temperature: float = float(os.getenv("TEMPERATURE", 0.0))
    notes_path: str = f"{os.getcwd()}/ai/data/data.txt"


env = Env()
