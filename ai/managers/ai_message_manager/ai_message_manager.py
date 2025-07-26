from ai.managers import DbManager
from ai.model import AiMessage


class AiMessageManager:
    table = "AI#MESSAGE"

    def save_data(self, data: AiMessage):
        DbManager().add_item({"table": self.table, "app_id": data.id, **data.to_dict()})
        return data
