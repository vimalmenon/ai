from boto3.dynamodb.conditions import Key

from ai.managers import DbManager
from ai.model import (
    DbServiceModel,
)
from ai.model.enums import DbKeys


class DbServiceManager:
    table = "DB_SERVICE"

    def save(self, data: DbServiceModel) -> DbServiceModel:
        DbManager().add_item(
            {
                DbKeys.Primary.value: self.table,
                DbKeys.Secondary.value: data.id,
                **data.to_dict(),
            }
        )
        return data

    def get(self) -> list[DbServiceModel]:
        items = DbManager().query_items(Key(DbKeys.Primary.value).eq(self.table))
        return [DbServiceModel.to_cls(item) for item in items]

    def delete_by_id(self, id: str) -> None:
        """This will delete the db service by id"""
        DbManager().remove_item(
            {DbKeys.Primary.value: self.table, DbKeys.Secondary.value: id}
        )
