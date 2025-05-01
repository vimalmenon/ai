from ai.exceptions.exceptions import ClientError, ServerError
from ai.managers import WorkflowManager
from ai.model import WorkflowModel, WorkflowSlimModel


class WorkflowService:

    def get_workflows(self) -> list[WorkflowModel]:
        """This List out all workflows details"""
        try:
            return WorkflowManager().get_workflows()
        except Exception as exc:
            raise ServerError(
                status_code=500,
                detail=f"Error fetching workflows: {str(exc)}",
            ) from None

    def get_workflow_by_id(self, id: str) -> WorkflowModel | None:
        """Get the workflow by ID"""
        try:
            return WorkflowManager().get_workflow_by_id(id)
        except Exception as exc:
            raise ServerError(
                status_code=500,
                detail=f"Error fetching workflow by ID: {str(exc)}",
            ) from None

    def create_workflow(self, data: WorkflowSlimModel) -> WorkflowModel:
        """Create workflow"""
        try:
            return WorkflowManager().create_workflow(data)
        except Exception as exc:
            raise ServerError(
                status_code=500,
                detail=f"Error creating workflow: {str(exc)}",
            ) from None

    def update_workflow(self, id, data):
        """Update workflow"""
        try:
            return WorkflowManager().update_workflow(id, data)
        except Exception as exc:
            raise ServerError(
                status_code=500,
                detail=f"Error updating workflow: {str(exc)}",
            ) from None

    def delete_workflows_by_id(self, id):
        """Delete the workflow by ID"""
        try:
            return WorkflowManager().delete_workflows_by_id(id)
        except ClientError as ce:
            raise ClientError(
                status_code=ce.status_code,
                detail=ce.detail,
            ) from ce
        except Exception as exc:
            raise ServerError(
                status_code=500,
                detail=f"Error deleting workflow by ID: {str(exc)}",
            ) from None
