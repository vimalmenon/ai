from logging import getLogger

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent

from ai.model import (
    WorkflowNodeRequest,
)
from ai.model.enums import WorkflowType
from ai.services.llm_service.llm_service import LlmService
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
            model=LlmService().get_llm(llm=node.llm),
            tools=[ToolService().get_tool_func(tool) for tool in node.tools],
            name=node.name,
            prompt=node.prompt,
        )
        prompt_template = ChatPromptTemplate(
            [SystemMessage(content=node.prompt or ""), MessagesPlaceholder("msgs")]
        )
        prompt_messages = prompt_template.invoke(
            {
                "msgs": [HumanMessage(content=node.message or "")],
            }
        )
        result = agent_llm.invoke(prompt_messages)
        logger.warning(self.__parse_response(result["messages"][-1]))
        return self.__parse_response(result["messages"][-1])

    def execute_llm(self, node: WorkflowNodeRequest) -> dict[str, str]:
        llm = LlmService().get_llm(
            llm=node.llm, structured_output=node.structured_output
        )
        prompt_template = ChatPromptTemplate(
            [SystemMessage(content=node.prompt or ""), MessagesPlaceholder("msgs")]
        )
        prompt_messages = prompt_template.invoke(
            {
                "msgs": [HumanMessage(content=node.message or "")],
            }
        )
        result = llm.invoke(prompt_messages)
        logger.warning(self.__parse_response(result))
        return self.__parse_response(result)

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
