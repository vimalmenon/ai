from typing import Self

from ai.model.base_model import Base


class SchedulerProcessModel(Base):
    id: str
    primary_key: str
    secondary_key: str
    action: str
    created_at: str
    processed_at: str | None

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "primary_key": self.primary_key,
            "secondary_key": self.secondary_key,
            "action": self.action,
            "created_at": self.created_at,
            "processed_at": self.processed_at,
        }

    @classmethod
    def to_cls(cls, data: dict) -> Self:
        return cls(
            id=data["id"],
            primary_key=data["primary_key"],
            secondary_key=data["secondary_key"],
            action=data["action"],
            created_at=data["created_at"],
            processed_at=data.get("processed_at"),
        )
