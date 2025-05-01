from ai.common import ClientError
from ai.managers.workflow_manager.workflow_manager import WorkflowManager
from ai.model import WorkflowNodeRequest
from ai.utilities import generate_uuid


class WorkflowNodeManager:
    def create_workflow_node(self, wf_id: str, body):
        """Create the workflow node"""
        workflow = WorkflowManager().get_workflow_by_id(wf_id)
        if not workflow:
            raise ClientError(
                status_code=404,
                detail=f"Workflow with ID {wf_id} not found.",
            )
        uuid = generate_uuid()
        workflow.nodes[uuid] = WorkflowNodeRequest.from_dict(body)
        return WorkflowManager().update_workflow_node(wf_id, workflow.nodes)

    def delete_workflow_nodes(self, wf_id, id):
        """Delete the workflow node by ID"""
        workflow = WorkflowManager().get_workflow_by_id(wf_id)
        if not workflow:
            raise ClientError(
                status_code=404,
                detail=f"Workflow with ID {wf_id} not found.",
            )
        node = workflow.nodes.get(id)
        if not node:
            raise ClientError(
                status_code=404,
                detail=f"Workflow node with ID {id} not found.",
            )
        del workflow.nodes[id]
        return WorkflowManager().update_workflow_node(wf_id, workflow.nodes)

    def update_workflow_node(self, wf_id, id, data):
        """Update the workflow node by ID"""
        workflow = WorkflowManager().get_workflow_by_id(wf_id)
        if not workflow:
            raise ClientError(
                status_code=404,
                detail=f"Workflow with ID {wf_id} not found.",
            )
        node = workflow.nodes.get(id)
        if not node:
            raise ClientError(
                status_code=404,
                detail=f"Workflow node with ID {id} not found.",
            )
        workflow.nodes[id] = WorkflowNodeRequest.from_dict(data)
        return WorkflowManager().update_workflow_node(wf_id, workflow.nodes)
