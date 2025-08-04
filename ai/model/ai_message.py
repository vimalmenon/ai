from ai.model.base_model import Base
from ai.model.enums import AiMessageType


class AiMessage(Base):
    id: str
    content: str
    type: AiMessageType
    total_token: str | None = None
    model_name: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.content = kwargs.get("content")
        self.type = kwargs.get("type")
        self.total_token = kwargs.get("total_token")
        self.model_name = kwargs.get("model_name")

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "total_token": self.total_token,
            "model_name": self.model_name,
            "type": self.type.value,
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
        )
