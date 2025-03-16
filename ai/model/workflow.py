from pydantic import BaseModel


class CreateWorkflowRequest(BaseModel):
    name: str


class UpdateWorkflowRequest(BaseModel):
    name: str
    detail: str | None
    complete: bool


class WorkflowNodeRequest(BaseModel):
    name: str
    prompt: str | None
    type: str | None
    llm: str | None
    connections: list[str] | None


class CreateNodeRequest(BaseModel):
    name: str
