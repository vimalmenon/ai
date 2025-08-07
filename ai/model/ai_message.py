from ai.model.base_model import Base
from ai.model.enums import AiMessageType


class AiMessage(Base):
    id: str
    content: str
    type: AiMessageType
    created_date: str
    total_token: str | None = None
    model_name: str | None = None
    tool_name: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.content = kwargs.get("content")
        self.type = kwargs.get("type")
        self.total_token = kwargs.get("total_token")
        self.model_name = kwargs.get("model_name")
        self.created_date = kwargs.get("created_date")
        self.tool_name = kwargs.get("tool_name")

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "total_token": self.total_token,
            "model_name": self.model_name,
            "tool_name": self.tool_name,
            "type": self.type.value,
            "created_date": self.created_date,
        }

    @classmethod
    def to_cls(cls, data: dict) -> "AiMessage":
        """Convert a dictionary to an AiMessage instance."""
        return cls(
            id=data.get("id"),
            content=data.get("content"),
            type=AiMessageType(data.get("type")),
            total_token=data.get("total_token"),
            model_name=data.get("model_name"),
            created_date=data.get("created_date"),
            tool_name=data.get("tool_name"),
        )


class AiMessageGroup(Base):
    config_id: str
    execute_id: str
    workflow_id: str
    messages: list[AiMessage]
