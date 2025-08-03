from boto3.dynamodb.conditions import Key

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

    def get_data(self, exec_id: str) -> list[AiMessage]:
        items = DbManager().query_items(Key("table").eq(f"{self.table}#{exec_id}"))
        return [AiMessage.to_cls(item) for item in items]
