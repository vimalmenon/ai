import traceback
from logging import getLogger

from ai.exceptions.exceptions import ClientError, ServerError
from ai.managers import WorkflowExecuteManager, WorkflowManager
from ai.model import (
    UpdateWorkflowRequest,
    WorkflowModel,
    WorkflowModelWithExecutedWorkflow,
    WorkflowSlimModel,
)

logger = getLogger(__name__)


class WorkflowService:

    def __attach_executed_workflow(
        self, workflow: WorkflowModel
    ) -> WorkflowModelWithExecutedWorkflow:
        executed_workflows = WorkflowExecuteManager().get_workflow(workflow.id)
        return WorkflowModelWithExecutedWorkflow(
            **workflow.to_dict(), executed_workflows=executed_workflows
        )

    def get_workflows(self) -> list[WorkflowModelWithExecutedWorkflow]:
        """This List out all workflows details"""
        try:
            return [
                self.__attach_executed_workflow(workflow)
                for workflow in WorkflowManager().get_workflows()
            ]
        except Exception as exc:
            logger.error(
                f"Error fetching workflows: {str(exc)}",
            )
            traceback.print_exc()
            raise ServerError(
                status_code=500,
                detail=f"Error fetching workflows: {str(exc)}",
            ) from None

    def get_workflow_by_id(self, id: str) -> WorkflowModelWithExecutedWorkflow | None:
        """Get the workflow by ID"""
        try:
            workflow = WorkflowManager().get_workflow_by_id(id)
            if workflow:
                return self.__attach_executed_workflow(workflow)
            return None
        except Exception as exc:
            logger.error(f"Error fetching workflow by ID: {str(exc)}")
            raise ServerError(
                status_code=500,
                detail=f"Error fetching workflow by ID: {str(exc)}",
            ) from None

    def create_workflow(self, data: WorkflowSlimModel) -> WorkflowModel:
        """Create workflow"""
        try:
            return WorkflowManager().create_workflow(data)
        except Exception as exc:
            logger.error(f"Error creating workflow: {str(exc)}")
            raise ServerError(
                status_code=500,
                detail=f"Error creating workflow: {str(exc)}",
            ) from None

    def update_workflow(
        self, id: str, data: UpdateWorkflowRequest
    ) -> WorkflowModel | None:
        """Update workflow"""
        try:
            WorkflowManager().update_workflow(id, data)
            return WorkflowManager().get_workflow_by_id(id)

        except Exception as exc:
            logger.error(f"Error updating workflow: {str(exc)}")
            raise ServerError(
                status_code=500,
                detail=f"Error updating workflow: {str(exc)}",
            ) from None

    def delete_workflows_by_id(self, id: str) -> None:
        """Delete the workflow by ID"""
        try:
            return WorkflowManager().delete_workflows_by_id(id)
        except ClientError as ce:
            logger.error(ce.detail)

            raise ClientError(
                status_code=ce.status_code,
                detail=ce.detail,
            ) from ce
        except Exception as exc:
            logger.error(f"Error deleting workflow by ID: {str(exc)}")
            raise ServerError(
                status_code=500,
                detail=f"Error deleting workflow by ID: {str(exc)}",
            ) from None
