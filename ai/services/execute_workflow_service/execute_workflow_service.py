from logging import getLogger

from langchain_core.messages.ai import AIMessage
from langgraph.prebuilt import create_react_agent

from ai.exceptions.exceptions import ClientError
from ai.model import ExecuteWorkflowModel, WorkflowNodeRequest
from ai.model.others import WorkflowType
from ai.services.llm_service.llm_service import LLmService
from ai.services.tool_service.tool_service import ToolService
from ai.services.workflow_service.workflow_service import WorkflowService
from ai.utilities import created_date, generate_uuid

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

    def __execute_node(self, node: WorkflowNodeRequest) -> None:
        if node.type == WorkflowType.Agent:
            self.__execute_agent_node(node)

    def __execute_agent_node(self, node: WorkflowNodeRequest) -> None:
        agent_llm = create_react_agent(
            model=LLmService(llm=node.llm).get_llm(),
            tools=[ToolService().get_tool_func(tool) for tool in node.tools],
            name=node.name,
            prompt="You are a helpful assistant",
        )
        result = agent_llm.invoke(
            {"messages": [{"role": "user", "content": node.prompt}]}
        )
        logger.warning(
            ExecuteWorkflowModel.to_cls(self.__parse_response(result["messages"][-1]))
        )

    def __parse_response(self, response: AIMessage) -> dict[str, str]:
        response_metadata = response.response_metadata
        return {
            "id": generate_uuid(),
            "content": str(response.content) or "",
            "model_name": response_metadata.get("model_name", ""),
            "name": response.name or "",
            "total_tokens": response_metadata.get("token_usage", {}).get(
                "total_tokens", ""
            ),
            "created_at": created_date(),
        }
