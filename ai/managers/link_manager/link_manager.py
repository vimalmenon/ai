from boto3.dynamodb.conditions import Key

from ai.exceptions.exceptions import ClientError
from ai.managers import DbManager
from ai.model import LinkGroup
from ai.model.enums import DbKeys, DbTable


class LinkManager:
    table = DbTable.AI_LINKS.value

    def get_links(self) -> list[LinkGroup]:
        items = DbManager().query_items(Key(DbKeys.Primary.value).eq(self.table))
        return [LinkGroup.to_cls(item) for item in items]

    def create_link_group(self, data: LinkGroup) -> None:
        DbManager().add_item(
            {
                DbKeys.Primary.value: self.table,
                DbKeys.Secondary.value: data.id,
                **data.to_dict(),
            }
        )

    def get_link_group_by_id(self, id: str) -> LinkGroup:
        item = DbManager().get_item({DbKeys.Primary.value: self.table, DbKeys.Secondary.value: id})
        if item:
            return LinkGroup.to_cls(item)
        raise ClientError(detail=f"Link with {id} not found")

    def delete_link_group(self, id: str) -> None:
        DbManager().remove_item(
            {
                DbKeys.Primary.value: self.table,
                DbKeys.Secondary.value: id,
            }
        )

    def delete_link(self, lg_id: str, id: str) -> None:
        item = DbManager().get_item(
            {DbKeys.Primary.value: self.table, DbKeys.Secondary.value: lg_id}
        )
        if item:
            item = LinkGroup.to_cls(item)
            updated_items = [link for link in item.links if link.id != id]
            item.links = updated_items
            self.update_link_group(item)
            return
        raise ClientError(detail=f"Link with {id} not found")

    def update_link_group(self, data: LinkGroup) -> None:
        (
            update_expression,
            expression_attribute_values,
            expression_attribute_names,
        ) = self.__get_updated_details(data)
        DbManager().update_item(
            Key={DbKeys.Primary.value: self.table, DbKeys.Secondary.value: data.id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
        )

    def __get_updated_details(self, data: LinkGroup) -> tuple:
        expression: dict = {}
        expression["links"] = {
            "name": "#links",
            "key": ":links",
            "value": [link.to_dict() for link in data.links],
        }
        update_expression = []
        expression_attribute_values = {}
        expression_attribute_names = {}
        for key, value in expression.items():
            update_expression.append(f"{value['name']} = {value['key']}")
            expression_attribute_values[value["key"]] = value["value"]
            expression_attribute_names[value["name"]] = key

        return (
            "set " + ", ".join(update_expression),
            expression_attribute_values,
            expression_attribute_names,
        )
