from ai.common.exceptions import ClientError, ServerError
from ai.managers import WorkflowNodeManager


class WorkflowNodeService:
    def delete_workflow_nodes(self, wf_id, id):
        """Delete the workflow node by ID"""
        try:
            return WorkflowNodeManager().delete_workflow_nodes(wf_id, id)
        except ClientError as ce:
            raise ClientError(
                status_code=ce.status_code,
                detail=ce.detail,
            ) from ce
        except Exception as e:
            raise ServerError(
                status_code=404,
                detail=f"Workflow node with ID {id} not found.",
            ) from e

    def create_workflow_node(self, wf_id, body):
        """Create the workflow node"""
        try:
            return WorkflowNodeManager().create_workflow_node(wf_id, body)
        except Exception as e:
            raise ServerError(
                status_code=500,
                detail=f"Error creating workflow node: {str(e)}",
            ) from e

    def update_workflow_node(self, wf_id, id, data):
        """Update the workflow node"""
        try:
            return WorkflowNodeManager().update_workflow_node(wf_id, id, data)
        except Exception as e:
            raise ServerError(
                status_code=500,
                detail=f"Error updating workflow node: {str(e)}",
            ) from e
