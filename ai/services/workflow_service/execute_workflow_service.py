from logging import getLogger

from ai.exceptions.exceptions import ClientError
from ai.managers import WorkflowExecuteManager
from ai.model import (
    CreateExecuteWorkflowRequest,
    ExecuteWorkflowModel,
    ExecuteWorkflowNodeModel,
    ResumeWorkflowRequest,
    WorkflowNodeRequest,
    WorkflowStatus,
)
from ai.model.others import WorkflowNodeStatus, WorkflowType
from ai.services.llm_execute.llm_execute_service import LLMExecuteService
from ai.services.workflow_service.workflow_service import WorkflowService
from ai.utilities import created_date, generate_uuid

logger = getLogger(__name__)


class ExecuteWorkflowService:

    def get(self, id: str) -> list[ExecuteWorkflowModel]:
        """This will get the executed workflow"""
        return WorkflowExecuteManager().get_workflow(id)

    def execute(
        self, id: str, data: CreateExecuteWorkflowRequest
    ) -> ExecuteWorkflowModel:
        """This will execute the workflow"""
        nodes = self.__validate_item_nodes_and_return(id)
        model = self.__create_execute_workflow_model(data)
        node_list: list[ExecuteWorkflowNodeModel] = []
        for _id, node in nodes.items():
            if node.is_start:
                self.__create_node_model(node, nodes, node_list)
        model.nodes = node_list
        logger.info(model)
        WorkflowExecuteManager().add_workflow(id, model)
        return model

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
                    status=WorkflowNodeStatus.NEW,
                    node=node,
                )
            )
            self.__create_node_model(node_map[node.next], node_map, node_list)
        else:
            node_list.append(
                ExecuteWorkflowNodeModel(
                    id=generate_uuid(),
                    status=WorkflowNodeStatus.NEW,
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

    def resume_execute(
        self, wf_id: str, id: str, data: ResumeWorkflowRequest
    ) -> ExecuteWorkflowModel | None:
        """This will resume the pending workflow"""
        workflow = WorkflowExecuteManager().get_workflow_by_id(wf_id, id)
        if workflow:
            for index, node in enumerate(workflow.nodes):
                if node.id == data.id:
                    if node.node.type == WorkflowType.HumanInput:
                        node.status = WorkflowNodeStatus.COMPLETED
                        node.content = data.data
                        node.started_at = created_date()
                        node.completed_at = created_date()
                        if len(workflow.nodes) > index + 1:
                            self.__process_next_node(node, workflow.nodes[index + 1])
                        break
                    elif node.node.type == WorkflowType.LLM:
                        self.__execute_llm_workflow_node(node)
                        if len(workflow.nodes) > index + 1:
                            self.__process_next_node(node, workflow.nodes[index + 1])
                        break
            WorkflowExecuteManager().update_workflow(wf_id, id, workflow)
            return workflow
        return None

    def __execute_llm_workflow_node(self, node: ExecuteWorkflowNodeModel) -> None:
        """This will execute the LLM workflow node"""
        node.started_at = created_date()
        content = LLMExecuteService().execute(node.node)
        node.content = content["content"]
        node.total_tokens = content["total_tokens"]
        node.status = WorkflowNodeStatus.COMPLETED
        node.completed_at = created_date()

    def __process_next_node(
        self, node: ExecuteWorkflowNodeModel, next_node: ExecuteWorkflowNodeModel
    ) -> None:
        if next_node.node.data_from_previous_node:
            next_node.node.message = node.content

    def delete(self, wf_id: str, id: str) -> None:
        """This will delete the execute workflow"""
        WorkflowExecuteManager().delete_workflow(wf_id, id)
