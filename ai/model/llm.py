from pydantic import BaseModel


class LLMData(BaseModel):
    name: str
    model: str


class LLMResponse(BaseModel):
    data: list[LLMData]
