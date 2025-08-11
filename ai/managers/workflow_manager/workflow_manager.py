from logging import getLogger
from typing import Any

from boto3.dynamodb.conditions import Key

from ai.exceptions.exceptions import ClientError
from ai.managers import DbManager
from ai.managers.workflow_manager.workflow_execute_manager import WorkflowExecuteManager
from ai.model import (
    UpdateWorkflowRequest,
    WorkflowModel,
    WorkflowModelWithExecutedWorkflow,
    WorkflowSlimModel,
)
from ai.model.enums import DbKeys, DbTable
from ai.utilities import created_date, generate_uuid

logger = getLogger(__name__)


class WorkflowManager:
    table = DbTable.AI_WORKFLOWS.value

    def get_workflows(self) -> list[WorkflowModelWithExecutedWorkflow]:
        """This List out all workflows details"""
        if items := DbManager().query_items(Key(DbKeys.Primary.value).eq(self.table)):
            workflows = [WorkflowModel.to_cls(item) for item in items]
            return [self.__attach_executed_workflow(workflow) for workflow in workflows]
        return []

    def __attach_executed_workflow(
        self, workflow: WorkflowModel
    ) -> WorkflowModelWithExecutedWorkflow:
        executed_workflows = WorkflowExecuteManager().get_workflow(workflow.id)
        return WorkflowModelWithExecutedWorkflow.use_workflow_cls(
            workflow, executed_workflows
        )

    def get_workflow_by_id(self, id: str) -> WorkflowModelWithExecutedWorkflow | None:
        """Get the workflow by ID"""
        if item := DbManager().get_item(
            {DbKeys.Primary.value: self.table, DbKeys.Secondary.value: id}
        ):
            return self.__attach_executed_workflow(WorkflowModel.to_cls(item))
        return None

    def create_workflow(
        self, data: WorkflowSlimModel
    ) -> WorkflowModelWithExecutedWorkflow:
        """Create workflow"""
        uuid = generate_uuid()
        item = WorkflowModel(id=uuid, name=data.name)
        DbManager().add_item(
            {
                DbKeys.Primary.value: self.table,
                DbKeys.Secondary.value: uuid,
                **item.to_dict(),
            }
        )
        return self.__attach_executed_workflow(item)

    def update_workflow(self, id: str, data: UpdateWorkflowRequest) -> None:
        """Update workflow"""
        if DbManager().get_item(
            {DbKeys.Primary.value: self.table, DbKeys.Secondary.value: id}
        ):
            (
                update_expression,
                expression_attribute_values,
                expression_attribute_names,
            ) = self.__get_workflow_details(data)
            DbManager().update_item(
                Key={DbKeys.Primary.value: self.table, DbKeys.Secondary.value: id},
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

    def delete_workflows_by_id(self, id: str) -> None:
        """Delete the workflow by ID"""
        db_manager = DbManager()
        if db_manager.get_item(
            {DbKeys.Primary.value: self.table, DbKeys.Secondary.value: id}
        ):
            db_manager.remove_item(
                {DbKeys.Primary.value: self.table, DbKeys.Secondary.value: id}
            )
        else:
            logger.warning(f"Workflow with ID {id} not found.")
            raise ClientError(
                status_code=404,
                detail=f"Workflow with ID {id} not found.",
            )

    def update_workflow_node(self, wf_id: str, nodes: dict) -> None:
        """Update the workflow node by ID"""
        DbManager().update_item(
            Key={DbKeys.Primary.value: self.table, DbKeys.Secondary.value: wf_id},
            UpdateExpression="set nodes= :nodes",
            ExpressionAttributeValues={":nodes": nodes},
        )

    def __get_workflow_details(
        self, data: WorkflowModel | UpdateWorkflowRequest
    ) -> tuple[str, dict, dict]:
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
