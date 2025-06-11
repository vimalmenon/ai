from logging import getLogger

from ai.exceptions.exceptions import ClientError, ServerError
from ai.managers import WorkflowNodeManager
from ai.model import CreateNodeRequest, WorkflowNodeRequest

logger = getLogger(__name__)


class WorkflowNodeService:
    def delete_workflow_nodes(self, wf_id: str, id: str) -> None:
        """Delete the workflow node by ID"""
        try:
            WorkflowNodeManager().delete_workflow_nodes(wf_id, id)
        except ClientError as ce:
            logger.error(f"Client error deleting workflow node: {str(ce)}")
            raise ClientError(
                status_code=ce.status_code,
                detail=ce.detail,
            ) from ce
        except Exception as e:
            logger.error(f"Error deleting workflow node: {str(e)}")
            raise ServerError(
                status_code=404,
                detail=f"Workflow node with ID {id} not found.",
            ) from e

    def create_workflow_node(self, wf_id: str, body: CreateNodeRequest) -> None:
        """Create the workflow node"""
        try:
            WorkflowNodeManager().create_workflow_node(wf_id, body)
        except Exception as e:
            logger.error(f"Error creating workflow node: {str(e)}")
            raise ServerError(
                status_code=500,
                detail=f"Error creating workflow node: {str(e)}",
            ) from e

    def update_workflow_node(
        self, wf_id: str, id: str, data: WorkflowNodeRequest
    ) -> None:
        """Update the workflow node"""
        try:
            WorkflowNodeManager().update_workflow_node(wf_id, id, data)
        except Exception as e:
            logger.error(f"Error updating workflow node: {str(e)}")
            raise ServerError(
                status_code=500,
                detail=f"Error updating workflow node: {str(e)}",
            ) from e
