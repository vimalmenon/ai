from logging import getLogger

from ai.managers import WorkflowNodeManager
from ai.model import (
    CreateNodeRequest,
    WorkflowModelWithExecutedWorkflow,
    WorkflowNodeRequest,
)
from ai.model.enums import Service, WorkflowType
from ai.services.workflow_service.workflow_service import WorkflowService

logger = getLogger(__name__)


class WorkflowNodeService:
    def delete_workflow_nodes(self, wf_id: str, id: str) -> None:
        """Delete the workflow node by ID"""
        WorkflowNodeManager().delete_workflow_nodes(wf_id, id)

    def create_workflow_node(self, wf_id: str, body: CreateNodeRequest) -> None:
        """Create the workflow node"""
        logger.info(body)
        WorkflowNodeManager().create_workflow_node(wf_id, body)

    def update_workflow_node(
        self, wf_id: str, id: str, data: WorkflowNodeRequest
    ) -> None:
        """Update the workflow node"""
        data.wf_id = wf_id
        result = self.__update_workflow_node_request(data)
        logger.info(result)
        WorkflowNodeManager().update_workflow_node(wf_id, id, result)

    def __update_workflow_node_request(
        self, data: WorkflowNodeRequest
    ) -> WorkflowNodeRequest:
        if data.type == WorkflowType.Service and (
            data.service == Service.GetFromDB or data.service == Service.GetFromS3
        ):
            data.request_at_run_time = True
        elif data.type == WorkflowType.Service and (
            data.service == Service.SaveToDB or data.service == Service.SaveToS3
        ):
            data.data_from_previous_node = True
        elif data.type == WorkflowType.HumanInput:
            data.request_at_run_time = True
        else:
            data.request_at_run_time = False
        return data

    def __get_workflow_by_id(self, wf_id: str) -> WorkflowModelWithExecutedWorkflow:
        return WorkflowService().get_workflow_by_id(wf_id)
