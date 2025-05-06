from logging import getLogger

from langgraph.prebuilt import create_react_agent

from ai.exceptions.exceptions import ClientError
from ai.llms import deepseek_llm
from ai.model import WorkflowNodeRequest
from ai.services.workflow_service.workflow_service import WorkflowService

logger = getLogger(__name__)


class ExecuteWorkflowService:
    def __init__(self, id: str):
        self.id = id

    def execute(self):
        nodes = self.__validate_item_nodes_and_return()
        for _id, node in nodes.items():
            self.__execute_node(node)
        return {"item": None}

    def resume_execute(self):
        self.__validate_item_nodes_and_return()

    def __validate_item_nodes_and_return(self) -> dict[str, WorkflowNodeRequest]:
        item = WorkflowService().get_workflow_by_id(self.id)
        if not item:
            raise ClientError(
                status_code=404,
                detail=f"Workflow with ID {id} not found.",
            )
        return item.nodes

    def __execute_node(self, node: WorkflowNodeRequest):
        if node.type == "agent":
            self.__execute_agent_node(node)

    def __execute_agent_node(self, node: WorkflowNodeRequest):
        agent_llm = create_react_agent(
            model=deepseek_llm,
            tools=[],
            name="resume_critique",
            prompt="You are a helpful assistant",
        )
        result = agent_llm.invoke(
            {"messages": [{"role": "user", "content": node.prompt}]}
        )
        logger.warning(result["messages"][-1])
