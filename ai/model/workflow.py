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

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            prompt=data.get("prompt"),
            type=data.get("type"),
            llm=data.get("llm"),
            tools=data.get("tools"),
            input=data.get("input"),
            next=data.get("next"),
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
    created_at: str | None = None
    nodes: dict[str, WorkflowNodeRequest] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.created_at = kwargs.get("created_at")
        self.detail = kwargs.get("detail")
        self.complete = kwargs.get("complete", False)
        self.nodes = kwargs.get("nodes", {})

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            detail=data.get("detail"),
            complete=data.get("complete", False),
            nodes=cls.__convert_nodes_from_dict(data.get("nodes", {})),
            created_at=data.get("created_at"),
        )

    @classmethod
    def __convert_nodes_from_dict(cls, nodes):
        items = {}
        for id, node in nodes.items():
            items[id] = WorkflowNodeRequest.from_dict(node)
        return items

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "detail": self.detail,
            "complete": self.complete,
            "nodes": self.__convert_nodes_to_dict(self.nodes),
            "created_at": self.created_at,
        }

    def __convert_nodes_to_dict(self, nodes):
        items = {}
        for id, node in nodes.items():
            items[id] = node.to_dict()
        return items


class WorkflowRequest(BaseModel):
    id: str
    name: str
    detail: str | None
    nodes: dict[str, WorkflowNodeRequest]
    complete: bool = False

    @classmethod
    def to_dict(cls):
        return {
            "id": cls.id,
            "name": cls.name,
            "detail": cls.detail,
            "nodes": [node.to_dict() for node in cls.nodes],
            "complete": cls.complete,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            detail=data.get("detail"),
            nodes=cls.__convert_nodes_to_class(data.get("nodes")),
            complete=data.get("complete", False),
        )

    def __convert_nodes_to_class(self, nodes):
        items = {}
        for id, node in nodes.items():
            items[id] = WorkflowNodeRequest().from_dict(node)
        return items


class CreateNodeRequest(BaseModel):
    name: str
