from pydantic import BaseModel

# from ai.model.enums import LLMs


class LLMData(BaseModel):
    name: str
    model: str
    supported: bool


class LLMResponse(BaseModel):
    data: list[LLMData]
