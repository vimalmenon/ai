from typing import Self

from ai.model.base_model import Base
from ai.model.enums import (
    LLMs,
    Service,
    StructuredOutputType,
    Tool,
    WorkflowNodeStatus,
    WorkflowStatus,
    WorkflowType,
)
from ai.utilities import created_date


class UpdateWorkflowRequest(Base):
    name: str
    detail: str | None
    complete: bool


class WorkflowNodeRequest(Base):
    id: str | None = None
    wf_id: str | None = None
    name: str
    prompt: str | None = None
    message: str | None = None
    type: WorkflowType | None = None
    llm: LLMs | None = None
    tools: list[Tool] = []
    tool: Tool | None = None
    next: str | None = None
    updated_at: str | None = None
    service: Service | None = None
    is_start: bool = False
    request_at_run_time: bool = False
    data_from_previous_node: bool = False
    structured_output: StructuredOutputType | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name")
        self.id = kwargs.get("id")
        self.wf_id = kwargs.get("wf_id")
        self.prompt = kwargs.get("prompt")
        self.message = kwargs.get("message")
        self.type = (
            WorkflowType[str(kwargs.get("type"))] if kwargs.get("type") else None
        )
        self.llm = LLMs[str(kwargs.get("llm"))] if kwargs.get("llm") else None
        self.tools = [Tool[tool] for tool in kwargs.get("tools", [])]
        self.tool = Tool[kwargs.get("tool")] if kwargs.get("tool") else None
        self.next = kwargs.get("next")
        self.updated_at = kwargs.get("updated_at", created_date())
        self.is_start = kwargs.get("is_start", False)
        self.service = (
            Service[str(kwargs.get("service"))] if kwargs.get("service") else None
        )
        self.request_at_run_time = kwargs.get("request_at_run_time", False)
        self.data_from_previous_node = kwargs.get("data_from_previous_node", False)
        self.structured_output = (
            StructuredOutputType[str(kwargs.get("structured_output"))]
            if kwargs.get("structured_output")
            else None
        )

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "id": self.id,
            "wf_id": self.wf_id,
            "name": self.name,
            "prompt": self.prompt,
            "message": self.message,
            "type": self.type.value if self.type else None,
            "llm": self.llm.value if self.llm else None,
            "tools": [tool.value for tool in self.tools],
            "tool": self.tool.value if self.tool else None,
            "next": self.next,
            "updated_at": self.updated_at,
            "is_start": self.is_start or False,
            "service": self.service.value if self.service else None,
            "request_at_run_time": self.request_at_run_time,
            "data_from_previous_node": self.data_from_previous_node,
            "structured_output": (
                self.structured_output.value if self.structured_output else None
            ),
        }

    @classmethod
    def to_cls(cls, data: dict) -> Self:
        """Convert a dictionary to a WorkflowNodeRequest object."""
        return cls(
            id=data.get("id"),
            wf_id=data.get("wf_id"),
            name=data.get("name"),
            prompt=data.get("prompt"),
            message=data.get("message"),
            type=data.get("type"),
            llm=data.get("llm"),
            tools=data.get("tools", []),
            tool=data.get("tool"),
            next=data.get("next"),
            updated_at=data.get("updated_at"),
            is_start=data.get("is_start"),
            service=data.get("service"),
            request_at_run_time=data.get("request_at_run_time"),
            data_from_previous_node=data.get("data_from_previous_node", False),
            structured_output=data.get("structured_output"),
        )


class WorkflowSlimModel(Base):
    name: str


class WorkflowModel(Base):
    id: str
    name: str
    detail: str | None = None
    complete: bool = False
    nodes: dict[str, WorkflowNodeRequest] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
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
        }

    def __convert_nodes_to_dict(self, nodes: dict[str, WorkflowNodeRequest]) -> dict:
        return {id: node.to_dict() for id, node in nodes.items()}


class CreateNodeRequest(Base):
    name: str


class CreateExecuteWorkflowRequest(Base):
    name: str


class ExecuteWorkflowNodeModel(Base):
    id: str
    exec_id: str
    content: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    task_id: str | None = None
    status: WorkflowNodeStatus
    node: WorkflowNodeRequest

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.exec_id = kwargs.get("exec_id")
        self.content = kwargs.get("content")
        self.status = kwargs.get("status")
        self.node = kwargs.get("node")
        self.started_at = kwargs.get("started_at")
        self.completed_at = kwargs.get("completed_at")
        self.task_id = kwargs.get("task_id")

    @classmethod
    def to_cls(cls, data: dict) -> Self:
        return cls(
            id=data.get("id", ""),
            exec_id=data.get("exec_id"),
            content=data.get("content"),
            status=(
                WorkflowNodeStatus[str(data.get("status"))]
                if data.get("status")
                else WorkflowNodeStatus.NEW
            ),
            node=WorkflowNodeRequest.to_cls(data.get("node", {})),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            task_id=data.get("task_id"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "exec_id": self.exec_id,
            "content": self.content,
            "status": (
                self.status.value if self.status else WorkflowNodeStatus.NEW.value
            ),
            "node": self.node.to_dict(),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "task_id": self.task_id,
        }


class ExecuteWorkflowModel(Base):
    id: str
    name: str
    created_at: str
    status: WorkflowStatus
    completed_at: str | None = None
    nodes: list[ExecuteWorkflowNodeModel] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id", "")
        self.name = kwargs.get("name", "")
        self.created_at = kwargs.get("created_at", created_date())
        self.status = WorkflowStatus[kwargs.get("status", WorkflowStatus.NEW.value)]
        self.completed_at = kwargs.get("completed_at")
        self.nodes = kwargs.get("nodes", [])

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "status": self.status.value,
            "completed_at": self.completed_at,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    @classmethod
    def to_cls(cls, data: dict) -> Self:
        """Convert a dictionary to an ExecuteWorkflowModel object."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            created_at=data.get("created_at", ""),
            status=data.get("status", ""),
            completed_at=data.get("completed_at"),
            nodes=[
                ExecuteWorkflowNodeModel.to_cls(node) for node in data.get("nodes", [])
            ],
        )


class WorkflowModelWithExecutedWorkflow(WorkflowModel):
    executed_workflows: list[ExecuteWorkflowModel]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.executed_workflows = kwargs.get("executed_workflows")

    @classmethod
    def use_workflow_cls(
        cls, data: WorkflowModel, executed_wf: list[ExecuteWorkflowModel]
    ) -> Self:
        return cls(
            id=data.id,
            name=data.name,
            detail=data.detail,
            complete=data.complete,
            nodes=data.nodes,
            executed_workflows=executed_wf,
        )

    # @property
    # def completed_workflow(self):
    #     return 5


class ExecuteWorkflowModelListData(Base):
    data: list[ExecuteWorkflowModel]


class ExecuteWorkflowModelData(Base):
    data: ExecuteWorkflowModel
