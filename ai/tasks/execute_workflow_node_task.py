from logging import getLogger

from ai.model import ExecuteWorkflowNodeModel, ResumeWorkflowRequest
from tasks import celery_app

logger = getLogger(__name__)


@celery_app.task
def execute_workflow_node_llm(node):
    from ai.services.llm_service.llm_execute_service import LLMExecuteService
    from ai.services.workflow_service.execute_workflow_service import (
        ExecuteWorkflowService,
    )

    logger.info(node)
    wf_node = ExecuteWorkflowNodeModel.to_cls(node)
    LLMExecuteService().execute(wf_node.exec_id, wf_node.node)
    data = ResumeWorkflowRequest(id=wf_node.id, data="COMPLETE")
    ExecuteWorkflowService().resume_execute(wf_node.node.wf_id, wf_node.exec_id, data)


@celery_app.task
def execute_workflow_node_agent(node):
    from ai.services.llm_service.llm_execute_service import LLMExecuteService
    from ai.services.workflow_service.execute_workflow_service import (
        ExecuteWorkflowService,
    )

    logger.info(node)
    wf_node = ExecuteWorkflowNodeModel.to_cls(node)
    LLMExecuteService().execute(wf_node.exec_id, wf_node.node)
    data = ResumeWorkflowRequest(id=wf_node.id, data="COMPLETE")
    ExecuteWorkflowService().resume_execute(wf_node.node.wf_id, wf_node.exec_id, data)
