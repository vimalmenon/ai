from boto3.dynamodb.conditions import Key

from ai.managers import DbManager
from ai.model import (
    DbServiceModel,
)


class DbServiceManager:
    table = "DB_SERVICE"

    def save(self, id: str, data: DbServiceModel) -> DbServiceModel:
        DbManager().add_item(
            {"table": f"{self.table}#{id}", "app_id": data.id, **data.to_dict()}
        )
        return data

    def get(self) -> list[DbServiceModel]:
        items = DbManager().query_items(
            Key("table").eq(self.table) & Key("app_id").begins_with(f"{id}#")
        )
        return [DbServiceModel.to_cls(item) for item in items]
