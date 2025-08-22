from boto3.dynamodb.conditions import Key

from ai.managers import DbManager
from ai.model import ExecuteWorkflowModel
from ai.model.enums import DbKeys, DbTable


class WorkflowExecuteManager:
    table = DbTable.AI_EXECUTE.value

    def add_workflow(self, id: str, data: ExecuteWorkflowModel) -> None:
        """This will save executed workflow"""
        DbManager().add_item(
            {
                DbKeys.Primary.value: self.table,
                DbKeys.Secondary.value: f"{id}#{data.id}",
                **data.to_dict(),
            }
        )

    def update_workflow(self, wf_id: str, id: str, data: ExecuteWorkflowModel) -> None:
        """This will update the executed workflow"""
        (
            update_expression,
            expression_attribute_values,
            expression_attribute_names,
        ) = self.__get_updated_executed_details(data)
        DbManager().update_item(
            Key={
                DbKeys.Primary.value: self.table,
                DbKeys.Secondary.value: f"{wf_id}#{id}",
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
        )

    def get_workflow(self, id: str) -> list[ExecuteWorkflowModel]:
        """This will get the executed workflow"""
        items = DbManager().query_items(
            Key(DbKeys.Primary.value).eq(self.table)
            & Key(DbKeys.Secondary.value).begins_with(f"{id}#")
        )
        return [ExecuteWorkflowModel.to_cls(item) for item in items]

    def get_workflow_by_id(self, wf_id: str, id: str) -> ExecuteWorkflowModel | None:
        """This will get the executed workflow by ID"""
        item = DbManager().get_item(
            {DbKeys.Primary.value: self.table, DbKeys.Secondary.value: f"{wf_id}#{id}"}
        )
        if item:
            return ExecuteWorkflowModel.to_cls(item)
        return None

    def delete_workflow(self, wf_id: str, id: str) -> None:
        """This will delete the executed workflow"""
        DbManager().remove_item(
            {
                DbKeys.Primary.value: self.table,
                DbKeys.Secondary.value: f"{wf_id}#{id}",
            }
        )

    def __get_updated_executed_details(self, data: ExecuteWorkflowModel) -> tuple[str, dict, dict]:
        expression: dict = {}
        if data.nodes:
            expression["nodes"] = {
                "name": "#nodes",
                "key": ":nodes",
                "value": [node.to_dict() for node in data.nodes],
            }
        if data.completed_at:
            expression["completed_at"] = {
                "name": "#completed_at",
                "key": ":completed_at",
                "value": data.completed_at,
            }
        if data.status:
            expression["status"] = {
                "name": "#status",
                "key": ":status",
                "value": data.status.value,
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
