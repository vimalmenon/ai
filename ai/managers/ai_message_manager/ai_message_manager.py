from boto3.dynamodb.conditions import Key

from ai.managers import DbManager
from ai.model import AiMessage
from ai.model.enums import DbKeys, DbTable


class AiMessageManager:
    table = DbTable.AI_MESSAGE.value

    def save_data(self, exec_id: str, data: AiMessage):
        DbManager().add_item(
            {
                DbKeys.Primary.value: f"{self.table}#{exec_id}",
                DbKeys.Secondary.value: f"{exec_id}#{data.id}",
                **data.to_dict(),
            }
        )
        return data

    def get_data(self, exec_id: str) -> list[AiMessage]:
        items = DbManager().query_items(
            Key(DbKeys.Primary.value).eq(f"{self.table}#{exec_id}")
        )
        return [AiMessage.to_cls(item) for item in items]
