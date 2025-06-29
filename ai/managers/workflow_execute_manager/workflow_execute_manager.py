from boto3.dynamodb.conditions import Key

from ai.managers import DbManager
from ai.model import ExecuteWorkflowModel


class WorkflowExecuteManager:
    table = "AI#EXECUTE"

    def add_workflow(self, id: str, data: ExecuteWorkflowModel):
        """This will save executed workflow"""
        DbManager().add_item(
            {"table": self.table, "app_id": f"{id}#{data.id}", **data.to_dict()}
        )

    def update_workflow(self, wf_id: str, id: str, data: ExecuteWorkflowModel):
        """This will update the executed workflow"""
        (
            update_expression,
            expression_attribute_values,
            expression_attribute_names,
        ) = self.__get_updated_executed_details(data)
        DbManager().update_item(
            Key={"table": self.table, "app_id": f"{wf_id}#{id}"},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
        )

    def get_workflow(self, id: str) -> list[ExecuteWorkflowModel]:
        """This will get the executed workflow"""
        items = DbManager().query_items(
            Key("table").eq(self.table) & Key("app_id").begins_with(f"{id}#")
        )
        return [ExecuteWorkflowModel.to_cls(item) for item in items]

    def get_workflow_by_id(self, wf_id: str, id: str):
        """This will get the executed workflow by ID"""
        item = DbManager().get_item({"table": self.table, "app_id": f"{wf_id}#{id}"})
        if item:
            return ExecuteWorkflowModel.to_cls(item)
        return None

    def delete_workflow(self, wf_id: str, id: str):
        """This will delete the executed workflow"""
        DbManager().remove_item(
            {
                "table": self.table,
                "app_id": f"{wf_id}#{id}",
            }
        )

    def __get_updated_executed_details(self, data: ExecuteWorkflowModel):
        expression: dict = {}
        if data.nodes:
            expression["nodes"] = {
                "name": "#nodes",
                "key": ":nodes",
                "value": data.nodes,
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
