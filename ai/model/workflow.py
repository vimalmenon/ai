from typing import Self

from pydantic import BaseModel

from ai.model.llm import LLMs
from ai.model.others import Tool, WorkflowType
from ai.utilities import created_date


class UpdateWorkflowRequest(BaseModel):
    name: str
    detail: str | None
    complete: bool


class WorkflowNodeRequest(BaseModel):
    id: str | None = None
    name: str
    prompt: str | None = None
    type: WorkflowType | None = None
    llm: LLMs | None = None
    tools: list[Tool] = []
    input: str | None = None
    next: list[str] = []
    updated_at: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name")
        self.id = kwargs.get("id")
        self.prompt = kwargs.get("prompt")
        self.type = (
            WorkflowType[str(kwargs.get("type"))] if kwargs.get("type") else None
        )
        self.llm = LLMs[str(kwargs.get("llm"))] if kwargs.get("llm") else None
        self.tools = [Tool[tool] for tool in kwargs.get("tools", [])]
        self.input = kwargs.get("input")
        self.next = kwargs.get("next", [])
        self.updated_at = kwargs.get("updated_at", created_date())

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "prompt": self.prompt,
            "type": self.type.value if self.type else None,
            "llm": self.llm.value if self.llm else None,
            "tools": [tool.value for tool in self.tools],
            "input": self.input,
            "next": self.next,
            "updated_at": self.updated_at,
        }

    @classmethod
    def to_cls(cls, data: dict) -> Self:
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            prompt=data.get("prompt"),
            type=data.get("type"),
            llm=data.get("llm"),
            tools=data.get("tools", []),
            input=data.get("input"),
            next=data.get("next"),
            updated_at=data.get("updated_at", created_date()),
        )


class WorkflowSlimModel(BaseModel):
    name: str

    def __init__(self, name: str):
        super().__init__(name=name)
        self.name = name


class WorkflowModel(BaseModel):
    id: str
    name: str
    detail: str | None = None
    complete: bool = False
    updated_at: str | None = None
    nodes: dict[str, WorkflowNodeRequest] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.updated_at = kwargs.get("updated_at", created_date())
        self.detail = kwargs.get("detail")
        self.complete = kwargs.get("complete", False)
        self.nodes = kwargs.get("nodes", {})

    @classmethod
    def to_cls(cls, data: dict) -> Self:
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            detail=data.get("detail"),
            complete=data.get("complete", False),
            nodes=cls.__convert_nodes_from_dict(data.get("nodes", {})),
            updated_at=data.get("updated_at", created_date()),
        )

    @classmethod
    def __convert_nodes_from_dict(cls, nodes: dict) -> dict[str, WorkflowNodeRequest]:
        """Convert nodes from dictionary to WorkflowNodeRequest objects."""
        return {id: WorkflowNodeRequest.to_cls(node) for id, node in nodes.items()}

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "detail": self.detail,
            "complete": self.complete,
            "nodes": self.__convert_nodes_to_dict(self.nodes),
            "updated_at": self.updated_at,
        }

    def __convert_nodes_to_dict(self, nodes: dict[str, WorkflowNodeRequest]) -> dict:
        return {id: node.to_dict() for id, node in nodes.items()}


class CreateNodeRequest(BaseModel):
    name: str


class ExecuteWorkflowModel(BaseModel):
    id: str
    name: str
    content: str
    created_at: str
    total_tokens: int
    model_name: str
    status: str

    @classmethod
    def to_cls(cls, data: dict[str, str]) -> Self:
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            content=data.get("content", ""),
            status="COMPLETE",
            total_tokens=int(data.get("total_tokens", "0")),
            model_name=data.get("model_name", ""),
            created_at=data.get("created_at", ""),
        )

    def to_dict(self) -> dict[str, str | int]:
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "status": self.status,
            "total_tokens": self.total_tokens,
            "model_name": self.model_name,
            "created_at": self.created_at,
        }
