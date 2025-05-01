from ai.managers import WorkflowNodeManager


class WorkflowNodeService:
    def delete_workflow_nodes(self, wf_id, id):
        """Delete the workflow node by ID"""
        return WorkflowNodeManager().delete_workflow_nodes(wf_id, id)

    def create_workflow_node(self, wf_id, body):
        """Create the workflow node"""
        return WorkflowNodeManager().create_workflow_node(wf_id, body)

    def update_workflow_node(self, wf_id, id, data):
        """Update the workflow node"""
        return WorkflowNodeManager().update_workflow_node(wf_id, id, data)
