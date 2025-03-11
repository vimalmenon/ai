import os

from pydantic import BaseModel


class Env(BaseModel):
    temperature: float = float(os.getenv("TEMPERATURE", 0.0))
    notes_path: str = f"{os.getcwd()}/ai/data/notes/data.txt"
    debug: bool = bool(os.getenv("DEBUG", False))
    table: str = str(os.getenv("TABLE"))
    aws_client_id: str = str(os.getenv("AWS_CLIENT_ID"))
    aws_secret: str = str(os.getenv("AWS_SECRET"))
    supported_llm: list[str] = os.getenv("SUPPORTED_LLM", "").split(",")


env = Env()
