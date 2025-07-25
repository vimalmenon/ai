from logging import getLogger

from langchain_core.messages.ai import AIMessage
from langgraph.prebuilt import create_react_agent

from ai.model import (
    WorkflowNodeRequest,
)
from ai.model.enums import WorkflowType
from ai.services.llm_service.llm_service import LLmService
from ai.services.tool_service.tool_service import ToolService
from ai.utilities import created_date, generate_uuid

logger = getLogger(__name__)


class LLMExecuteService:

    def execute(self, node: WorkflowNodeRequest) -> dict[str, str]:
        if node.type == WorkflowType.LLM:
            return self.execute_llm(node)
        else:
            return self.execute_agent(node)

    def execute_agent(self, node: WorkflowNodeRequest) -> dict[str, str]:
        agent_llm = create_react_agent(
            model=LLmService().get_llm(llm=node.llm),
            tools=[ToolService().get_tool_func(tool) for tool in node.tools],
            name=node.name,
            prompt=node.prompt,
        )
        result = agent_llm.invoke(
            {"messages": [{"role": "user", "content": node.message}]}
        )
        logger.warning(self.__parse_response(result["messages"][-1]))
        return self.__parse_response(result["messages"][-1])

    def execute_llm(self, node: WorkflowNodeRequest) -> dict[str, str]:
        llm = LLmService().get_llm(
            llm=node.llm, structured_output=node.structured_output
        )
        result = llm.invoke({"messages": [{"role": "user", "content": node.message}]})
        logger.warning(self.__parse_response(result["messages"][-1]))
        return self.__parse_response(result["messages"][-1])

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
