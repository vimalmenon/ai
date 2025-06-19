from logging import getLogger

from ai.exceptions.exceptions import ClientError
from ai.managers import WorkflowExecuteManager
from ai.model import (
    CreateExecuteWorkflowRequest,
    ExecuteWorkflowModel,
    ExecuteWorkflowNodeModel,
    WorkflowNodeRequest,
    WorkflowStatus,
)
from ai.services.workflow_service.workflow_service import WorkflowService
from ai.utilities import created_date, generate_uuid

logger = getLogger(__name__)


class ExecuteWorkflowService:

    def get(self, id: str):
        """This will get the execute workflow"""
        items = WorkflowExecuteManager().get_workflow(id)
        return [ExecuteWorkflowModel.to_cls(item) for item in items]

    def execute(self, id: str, data: CreateExecuteWorkflowRequest):
        nodes = self.__validate_item_nodes_and_return(id)
        model = self.__create_execute_workflow_model(data)
        _node_list: list[ExecuteWorkflowNodeModel] = []
        for _id, node in nodes.items():
            if node.is_start:
                self.__create_node_model(node, nodes, _node_list)
                breakpoint()
        logger.info(model)
        # WorkflowExecuteManager().execute_workflow(id, model)
        return {"item": nodes}

    def __create_node_model(
        self,
        node: WorkflowNodeRequest,
        node_map: dict[str, WorkflowNodeRequest],
        node_list: list[ExecuteWorkflowNodeModel],
    ) -> None:
        if node.next:
            node_list.append(
                ExecuteWorkflowNodeModel(
                    id=generate_uuid(),
                    name=node.name,
                    status=WorkflowStatus.NEW.value,
                    node=node,
                )
            )
            self.__create_node_model(node_map[node.next], node_map, node_list)
        else:
            node_list.append(
                ExecuteWorkflowNodeModel(
                    id=generate_uuid(),
                    name=node.name,
                    status=WorkflowStatus.NEW.value,
                    node=node,
                )
            )

    def __validate_item_nodes_and_return(
        self, id: str
    ) -> dict[str, WorkflowNodeRequest]:
        item = WorkflowService().get_workflow_by_id(id)
        if not item:
            raise ClientError(
                status_code=404,
                detail=f"Workflow with ID {id} not found.",
            )
        return item.nodes

    def __create_execute_workflow_model(
        self, data: CreateExecuteWorkflowRequest
    ) -> ExecuteWorkflowModel:
        """
        Create a new ExecuteWorkflowModel instance with default values.
        """
        return ExecuteWorkflowModel(
            id=generate_uuid(),
            name=data.name,
            created_at=created_date(),
            status=WorkflowStatus.RUNNING.value,
        )

    def resume_execute(self, id: str):
        self.__validate_item_nodes_and_return(id)

    def delete(self, wf_id: str, id: str):
        """This will delete the execute workflow"""
        return WorkflowExecuteManager().delete_workflow(wf_id, id)
