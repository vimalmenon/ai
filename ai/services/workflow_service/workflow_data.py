from ai.model.base_db import BaseDb


class WorkflowDBItem(BaseDb):
    id: str
    name: str
    detail: str

    def __init__(self, table, app_id, id, name, detail):
        super().__init__(table, app_id, id, name, detail)
        self.id = id
        self.name = name
        self.detail = detail

    def to_json(self):
        return {
            "table": self.table,
            "app_id": self.app_id,
            "id": self.id,
            "name": self.name,
            "detail": self.detail,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
        }
