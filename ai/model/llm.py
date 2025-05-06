from enum import Enum

from pydantic import BaseModel


class LLMs(Enum):
    DEEPSEEK = "DEEPSEEK"
    GOOGLE = "GOOGLE"
    OLLAMA = "OLLAMA"


class LLMData(BaseModel):
    name: str
    model: str
    supported: bool


class LLMResponse(BaseModel):
    data: list[LLMData]
