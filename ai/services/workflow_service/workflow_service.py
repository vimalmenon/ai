from logging import getLogger

from ai.exceptions.exceptions import ClientError
from ai.managers import WorkflowManager
from ai.model import (
    UpdateWorkflowRequest,
    WorkflowModel,
    WorkflowModelWithExecutedWorkflow,
    WorkflowSlimModel,
)

logger = getLogger(__name__)


class WorkflowService:

    def get_workflows(self) -> list[WorkflowModelWithExecutedWorkflow]:
        """This List out all workflows details"""
        return WorkflowManager().get_workflows()

    def get_workflow_by_id(self, id: str) -> WorkflowModelWithExecutedWorkflow:
        """Get the workflow by ID"""
        if workflow := WorkflowManager().get_workflow_by_id(id):
            return workflow
        raise ClientError(detail=f"Workflow with id : {id} not found")

    def create_workflow(self, data: WorkflowSlimModel) -> WorkflowModel:
        """Create workflow"""
        return WorkflowManager().create_workflow(data)

    def update_workflow(
        self, id: str, data: UpdateWorkflowRequest
    ) -> WorkflowModelWithExecutedWorkflow | None:
        """Update workflow"""
        if self.get_workflow_by_id(id):
            WorkflowManager().update_workflow(id, data)
            return WorkflowManager().get_workflow_by_id(id)
        raise ClientError(detail=f"Workflow with id : {id} not found")

    def delete_workflows_by_id(self, id: str) -> None:
        """Delete the workflow by ID"""
        if item := self.get_workflow_by_id(id):
            if len(item.executed_workflows) == 0:
                WorkflowManager().delete_workflows_by_id(id)
                return None
            else:
                raise ClientError(
                    "Workflow has executed workflows and cannot be deleted"
                )
        raise ClientError(detail=f"Workflow with id : {id} not found")
