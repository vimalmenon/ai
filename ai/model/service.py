from typing import Self

from ai.model.base_model import Base


class DbServiceModel(Base):
    id: str
    data: str
    created_date: str
    wf_id: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "data": self.data,
            "wf_id": self.wf_id,
            "created_date": self.created_date,
        }

    @classmethod
    def to_cls(cls, data: dict) -> Self:
        return cls(
            id=data.get("id", ""),
            data=data.get("data", ""),
            created_date=data.get("created_date", ""),
            wf_id=data.get("wf_id", ""),
        )
