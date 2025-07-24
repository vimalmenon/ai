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
from ai.model.enums import Service as ServiceModel
from ai.model.enums import WorkflowNodeStatus, WorkflowType
from ai.services.llm_execute.llm_execute_service import LLMExecuteService
from ai.services.service.db_service import DbService
from ai.services.workflow_service.workflow_service import WorkflowService
from ai.utilities import created_date, generate_uuid

logger = getLogger(__name__)


class ExecuteWorkflowService:

    def get(self, id: str) -> list[ExecuteWorkflowModel]:
        """This will get the executed workflow"""
        return WorkflowExecuteManager().get_workflow(id)

    def get_executed_workflow_id(self, wf_id: str, id: str) -> ExecuteWorkflowModel:
        """This will get by executed id"""
        item = WorkflowExecuteManager().get_workflow_by_id(wf_id, id)
        if item:
            return item
        raise ClientError(detail=f"Unable to find Executed Workflow with {wf_id} {id}")

    def execute(
        self, id: str, data: CreateExecuteWorkflowRequest
    ) -> ExecuteWorkflowModel:
        """This will execute the workflow"""
        nodes = self.__validate_item_nodes_and_return(id)
        model = self.__create_execute_workflow_model(data)
        node_list: list[ExecuteWorkflowNodeModel] = []
        for _id, node in nodes.items():
            if node.is_start:
                self.__create_node_model(node, nodes, node_list, True)
        model.nodes = node_list
        logger.info(model)
        WorkflowExecuteManager().add_workflow(id, model)
        return model

    def __create_node_model(
        self,
        node: WorkflowNodeRequest,
        node_map: dict[str, WorkflowNodeRequest],
        node_list: list[ExecuteWorkflowNodeModel],
        is_start: bool,
    ) -> None:
        if node.next:
            node_list.append(
                ExecuteWorkflowNodeModel(
                    id=generate_uuid(),
                    status=(
                        WorkflowNodeStatus.READY if is_start else WorkflowNodeStatus.NEW
                    ),
                    node=node,
                )
            )
            self.__create_node_model(node_map[node.next], node_map, node_list, False)
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
            [
                self.__process_workflow_node(index, node, workflow, data)
                for index, node in enumerate(workflow.nodes)
                if node.id == data.id
            ]
            WorkflowExecuteManager().update_workflow(wf_id, id, workflow)
            return workflow
        raise ClientError(
            status_code=404,
            detail=f"Workflow with ID {wf_id} not found.",
        )

    def __process_workflow_node(
        self,
        index: int,
        node: ExecuteWorkflowNodeModel,
        workflow: ExecuteWorkflowModel,
        data: ResumeWorkflowRequest,
    ) -> bool:
        if node.node.type == WorkflowType.HumanInput:
            node.status = WorkflowNodeStatus.COMPLETED
            node.content = data.data
            node.started_at = created_date()
            node.completed_at = created_date()
            if len(workflow.nodes) > index + 1:
                self.__process_next_node(node, workflow.nodes[index + 1])
            self.__check_if_workflow_is_completed(index, workflow)
        elif node.node.type == WorkflowType.LLM:
            self.__execute_llm_workflow_node(node)
            if len(workflow.nodes) > index + 1:
                self.__process_next_node(node, workflow.nodes[index + 1])
            self.__check_if_workflow_is_completed(index, workflow)
        elif node.node.type == WorkflowType.Service:
            self.__execute_service_workflow_node(workflow.id, node, data)
            if len(workflow.nodes) > index + 1:
                self.__process_next_node(node, workflow.nodes[index + 1])
            self.__check_if_workflow_is_completed(index, workflow)
        return True

    def __execute_service_workflow_node(
        self, id: str, node: ExecuteWorkflowNodeModel, data: ResumeWorkflowRequest
    ) -> None:
        if node.node.service == ServiceModel.GetFromDB:
            node.started_at = created_date()
            node.status = WorkflowNodeStatus.COMPLETED
            node.content = data.data
            node.completed_at = created_date()
        elif node.node.service == ServiceModel.SaveToDB:
            node.started_at = created_date()
            content = DbService().execute(id, node.node)
            node.content = content["data"]
            node.status = WorkflowNodeStatus.COMPLETED
            node.completed_at = created_date()
        else:
            node.started_at = created_date()
            node.status = WorkflowNodeStatus.COMPLETED
            node.completed_at = created_date()

    def __execute_llm_workflow_node(self, node: ExecuteWorkflowNodeModel) -> None:
        """This will execute the LLM workflow node"""
        node.started_at = created_date()
        content = LLMExecuteService().execute(node.node)
        node.content = content["content"]
        node.total_tokens = int(content["total_tokens"])
        node.status = WorkflowNodeStatus.COMPLETED
        node.completed_at = created_date()

    def __check_if_workflow_is_completed(
        self, index: int, workflow: ExecuteWorkflowModel
    ) -> None:
        """Check if the workflow is completed"""
        if index == len(workflow.nodes) - 1:
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = created_date()

    def __process_next_node(
        self, node: ExecuteWorkflowNodeModel, next_node: ExecuteWorkflowNodeModel
    ) -> None:
        next_node.status = WorkflowNodeStatus.READY
        if next_node.node.data_from_previous_node:
            next_node.node.message = node.content

    def delete(self, wf_id: str, id: str) -> None:
        """This will delete the execute workflow"""
        WorkflowExecuteManager().delete_workflow(wf_id, id)
