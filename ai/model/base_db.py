from abc import ABC

from ai.utilities import created_date


class BaseDb(ABC):
    table: str
    app_id: str
    created_date: str
    updated_date: str | None

    def __init__(self, table, app_id, **kwargs):
        super().__init__()
        self.table = table
        self.app_id = app_id
        self.created_date = kwargs.get("created_date") or created_date()
        self.updated_date = kwargs.get("updated_date")
