import os

from pydantic import BaseModel


class Env(BaseModel):
    temperature: float = float(os.getenv("TEMPERATURE", 0.0))
    notes_path: str = f"{os.getcwd()}/ai/data/notes/data.txt"
    table = os.getenv("TABLE")
    aws_client_id = os.getenv("AWS_CLIENT_ID")
    aws_secret = os.getenv("AWS_SECRET")


env = Env()
