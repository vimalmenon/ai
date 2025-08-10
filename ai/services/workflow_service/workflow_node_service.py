from logging import getLogger

from ai.managers import WorkflowNodeManager
from ai.model import (
    CreateNodeRequest,
    WorkflowNodeRequest,
)
from ai.model.enums import Service, WorkflowType

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
        if data.type == WorkflowType.Service:
            return self.__update_workflow_node_service_request(data)
        return data

    def __update_workflow_node_service_request(
        self, data: WorkflowNodeRequest
    ) -> WorkflowNodeRequest:
        if data.service in [
            Service.GetFromDB,
            Service.GetFromS3,
            Service.SaveToDB,
            Service.SaveToS3,
            Service.HumanInput,
            Service.ManualConfirmation,
        ]:
            data.request_at_run_time = True
        else:
            data.request_at_run_time = False

        return data
