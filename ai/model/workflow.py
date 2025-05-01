from pydantic import BaseModel


class UpdateWorkflowRequest(BaseModel):
    name: str
    detail: str | None
    complete: bool


class WorkflowNodeRequest(BaseModel):
    id: str | None = None
    name: str
    prompt: str | None = None
    type: str | None = None
    llm: str | None = None
    tools: list[str] = []
    input: str | None = None
    next: list[str] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name")
        self.id = kwargs.get("id")
        self.prompt = kwargs.get("prompt")
        self.type = kwargs.get("type")
        self.llm = kwargs.get("llm")
        self.tools = kwargs.get("tools", [])
        self.input = kwargs.get("input")
        self.next = kwargs.get("next", [])

    def to_dict(self):
        return {
            "id": self.id,
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
            id=data.get("id"),
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


class CreateNodeRequest(BaseModel):
    name: str
