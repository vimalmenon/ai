from logging import getLogger
from typing import Any

from boto3.dynamodb.conditions import Key

from ai.exceptions.exceptions import ClientError
from ai.managers import DbManager
from ai.model import UpdateWorkflowRequest, WorkflowModel, WorkflowSlimModel
from ai.utilities import created_date, generate_uuid

logger = getLogger(__name__)


class WorkflowManager:
    table = "AI#WORKFLOWS"

    def get_workflows(self) -> list[WorkflowModel]:
        """This List out all workflows details"""
        items = DbManager().query_items(Key("table").eq(self.table))
        if not items:
            return []
        return [WorkflowModel.to_cls(item) for item in items]

    def get_workflow_by_id(self, id: str) -> WorkflowModel | None:
        """Get the workflow by ID"""
        item = DbManager().get_item({"table": self.table, "app_id": id})
        if item:
            return WorkflowModel.to_cls(item)
        return None

    def create_workflow(self, data: WorkflowSlimModel) -> WorkflowModel:
        """Create workflow"""
        uuid = generate_uuid()
        item = WorkflowModel(id=uuid, name=data.name)
        DbManager().add_item({"table": self.table, "app_id": uuid, **item.to_dict()})
        return item

    def update_workflow(self, id: str, data: UpdateWorkflowRequest) -> None:
        """Update workflow"""
        item = DbManager().get_item({"table": self.table, "app_id": id})
        if item:
            (
                update_expression,
                expression_attribute_values,
                expression_attribute_names,
            ) = self.__get_workflow_details(data)
            DbManager().update_item(
                Key={"table": self.table, "app_id": id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names,
            )
        else:
            logger.warning(f"Workflow with ID {id} not found.")
            raise ClientError(
                status_code=404,
                detail=f"Workflow with ID {id} not found.",
            )

    def delete_workflows_by_id(self, id: str):
        """Delete the workflow by ID"""
        item = DbManager().get_item({"table": self.table, "app_id": id})
        if item:
            return DbManager().remove_item({"table": self.table, "app_id": id})
        else:
            logger.warning(f"Workflow with ID {id} not found.")
            raise ClientError(
                status_code=404,
                detail=f"Workflow with ID {id} not found.",
            )

    def update_workflow_node(self, wf_id: str, nodes: dict) -> None:
        """Update the workflow node by ID"""
        DbManager().update_item(
            Key={"table": self.table, "app_id": wf_id},
            UpdateExpression="set nodes= :nodes",
            ExpressionAttributeValues={":nodes": nodes},
        )

    def __get_workflow_details(self, data: WorkflowModel | UpdateWorkflowRequest):
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
        expression["updated_at"] = {
            "name": "#updated_at",
            "key": ":updated_at",
            "value": created_date(),
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
