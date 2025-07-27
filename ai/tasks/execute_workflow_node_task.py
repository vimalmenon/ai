from ai.model.workflow import ExecuteWorkflowNodeModel
from tasks import celery_app


@celery_app.task
def execute_workflow_node_llm(node):
    from ai.services.llm_execute.llm_execute_service import LLMExecuteService

    wf_node = ExecuteWorkflowNodeModel.to_cls(node)
    LLMExecuteService().execute(wf_node.exec_id, wf_node.node)


@celery_app.task
def execute_workflow_node_agent(node):
    from ai.services.llm_execute.llm_execute_service import LLMExecuteService

    wf_node = ExecuteWorkflowNodeModel.to_cls(node)
    LLMExecuteService().execute(wf_node.exec_id, wf_node.node)
