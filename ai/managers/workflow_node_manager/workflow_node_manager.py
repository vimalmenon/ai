from ai.common import ClientError
from ai.managers.workflow_manager.workflow_manager import WorkflowManager


class WorkflowNodeManager:
    def create_workflow_node(self, wf_id: str, body):
        pass

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
        pass
