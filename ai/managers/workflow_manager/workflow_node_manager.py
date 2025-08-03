from ai.exceptions.exceptions import ClientError
from ai.managers.workflow_manager.workflow_manager import WorkflowManager
from ai.model import CreateNodeRequest, WorkflowModel, WorkflowNodeRequest
from ai.utilities import generate_uuid


class WorkflowNodeManager:
    def create_workflow_node(self, wf_id: str, body: CreateNodeRequest) -> None:
        """Create the workflow node"""
        workflow = self.__validate_and_return_workflow(wf_id)
        uuid = generate_uuid()
        workflow.nodes[uuid] = WorkflowNodeRequest(id=uuid, wf_id=wf_id, name=body.name)
        WorkflowManager().update_workflow_node(
            wf_id, self.__convert_nodes_to_dict(workflow.nodes)
        )

    def delete_workflow_nodes(self, wf_id: str, id: str) -> None:
        """Delete the workflow node by ID"""
        workflow = self.__validate_and_return_workflow(wf_id)
        self.__validate_and_return_node(workflow, id)
        del workflow.nodes[id]
        WorkflowManager().update_workflow_node(
            wf_id, self.__convert_nodes_to_dict(workflow.nodes)
        )

    def update_workflow_node(self, wf_id, id, data: WorkflowNodeRequest) -> None:
        """Update the workflow node by ID"""
        workflow = self.__validate_and_return_workflow(wf_id)
        self.__validate_and_return_node(workflow, id)
        workflow.nodes[id] = data
        WorkflowManager().update_workflow_node(
            wf_id, self.__convert_nodes_to_dict(workflow.nodes)
        )

    def __validate_and_return_workflow(self, wf_id: str) -> WorkflowModel:
        """Validate the workflow"""
        workflow = WorkflowManager().get_workflow_by_id(wf_id)
        if not workflow:
            raise ClientError(
                status_code=404,
                detail=f"Workflow with ID {wf_id} not found.",
            )
        return workflow

    def __validate_and_return_node(
        self, workflow: WorkflowModel, id: str
    ) -> WorkflowNodeRequest:
        """Validate the workflow node"""
        node = workflow.nodes.get(id)
        if not node:
            raise ClientError(
                status_code=404,
                detail=f"Workflow node with ID {id} not found.",
            )
        return node

    def __convert_nodes_to_dict(self, nodes: dict[str, WorkflowNodeRequest]) -> dict:
        """Convert nodes to dictionary"""
        return {key: node.to_dict() for key, node in nodes.items()}
