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
    tools: list[str] | None
    input: str | None
    next: list[str] | None

    def to_dict(self):
        return {
            "name": self.name,
            "prompt": self.prompt,
            "type": self.type,
            "llm": self.llm,
            "tools": self.tools,
            "input": self.input,
            "next": self.next,
        }


class CreateNodeRequest(BaseModel):
    name: str
