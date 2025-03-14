from dataclasses import dataclass


@dataclass
class WorkflowItem:
    name: str
    id: str
    wf_name: str
    detail: str

    def to_json(self):
        return {
            "name": self.name,
            "id": self.id,
            "wf_name": self.name,
            "detail": self.detail,
        }
