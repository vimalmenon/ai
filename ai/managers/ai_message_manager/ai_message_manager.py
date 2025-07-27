from ai.managers import DbManager
from ai.model import AiMessage


class AiMessageManager:
    table = "AI#MESSAGE"

    def save_data(self, exec_id: str, data: AiMessage):
        DbManager().add_item(
            {
                "table": f"{self.table}#{exec_id}",
                "app_id": f"{exec_id}#{data.id}",
                **data.to_dict(),
            }
        )
        return data
