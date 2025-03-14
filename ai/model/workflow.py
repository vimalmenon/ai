from pydantic import BaseModel


class CreateWorkflowRequest(BaseModel):
    name: str
    detail: str
