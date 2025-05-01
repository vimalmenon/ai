from typing import Any

from boto3.dynamodb.conditions import Key
from fastapi import HTTPException

from ai.managers import DbManager
from ai.model import WorkflowModel, WorkflowSlimModel
from ai.utilities import generate_uuid


class WorkflowManager:
    table = "AI#WORKFLOWS"

    def get_workflows(self) -> list[WorkflowModel]:
        """This List out all workflows details"""
        items = DbManager().query_items(Key("table").eq(self.table))
        if not items:
            return []
        return [WorkflowModel.from_dict(item) for item in items]

    def get_workflow_by_id(self, id: str) -> WorkflowModel | None:
        """Get the workflow by ID"""
        item = DbManager().get_item({"table": self.table, "app_id": id})
        if item:
            return WorkflowModel.from_dict(item)
        return None

    def create_workflow(self, data: WorkflowSlimModel):
        """Create workflow"""
        uuid = generate_uuid()
        item = WorkflowModel(id=uuid, name=data.name)
        DbManager().add_item({"table": self.table, "app_id": uuid, **item.to_dict()})
        return item.to_dict()

    def update_workflow(self, id, data: WorkflowModel):
        """Update workflow"""
        item = DbManager().get_item({"table": self.table, "app_id": id})
        if item:
            (
                update_expression,
                expression_attribute_values,
                expression_attribute_names,
            ) = self._get_workflow_details(data)
            DbManager().update_item(
                Key={"table": self.table, "app_id": id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names,
            )
            return item
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Workflow with ID {id} not found.",
            )

    def delete_workflows_by_id(self, id: str):
        """Delete the workflow by ID"""
        return DbManager().remove_item({"table": self.table, "app_id": id})

    def update_workflow_node(self, wf_id: str, nodes):
        """Update the workflow node by ID"""
        DbManager().update_item(
            Key={"table": self.table, "app_id": wf_id},
            UpdateExpression="set nodes= :nodes",
            ExpressionAttributeValues={":nodes": nodes},
        )
        return nodes

    def _get_workflow_details(self, data: WorkflowModel):
        expression: dict[str, Any] = {}
        if data.name:
            expression["name"] = {
                "name": "#name",
                "key": ":name",
                "value": data.name,
            }
        if data.detail:
            expression["detail"] = {
                "name": "#detail",
                "key": ":detail",
                "value": data.detail,
            }
        if data.complete is not None:
            expression["complete"] = {
                "name": "#complete",
                "key": ":complete",
                "value": data.complete,
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
