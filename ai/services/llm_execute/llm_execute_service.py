from logging import getLogger

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent

from ai.managers.ai_message_manager.ai_message_manager import AiMessageManager
from ai.model import AiMessage, WorkflowNodeRequest
from ai.model.enums import AiMessageType, WorkflowType
from ai.services.llm_service.llm_service import LlmService
from ai.services.tool_service.tool_service import ToolService
from ai.utilities import generate_uuid

logger = getLogger(__name__)


class LLMExecuteService:

    def execute(self, exec_id: str, node: WorkflowNodeRequest) -> None:
        if node.type == WorkflowType.LLM:
            self.execute_llm(exec_id, node)
        else:
            self.execute_agent(exec_id, node)

    def execute_agent(self, exec_id: str, node: WorkflowNodeRequest) -> None:
        llm = LlmService().get_llm(
            llm=node.llm, structured_output=node.structured_output
        )
        agent_llm = create_react_agent(
            model=llm,
            tools=[ToolService().get_tool_func(tool) for tool in node.tools],
            name=node.name,
            prompt=node.prompt,
        )
        prompt_messages = self.__get_messages(node)
        for step in agent_llm.stream(prompt_messages, stream_mode="values"):
            logger.warning(step)
            result = step["messages"][-1]
            message = AiMessage(
                id=generate_uuid(), content=result.content, type=AiMessageType.AI
            )
            AiMessageManager().save_data(exec_id, message)

    def execute_llm(self, exec_id: str, node: WorkflowNodeRequest) -> None:
        llm = LlmService().get_llm(
            llm=node.llm, structured_output=node.structured_output
        )
        prompt_messages = self.__get_messages(node)
        result = llm.invoke(prompt_messages)
        logger.warning(result)
        message = AiMessage(
            id=result.id,
            content=result.content,
            model_name=result.response_metadata.get("model_name"),
            type=AiMessageType.AI,
        )
        AiMessageManager().save_data(
            exec_id,
            message,
        )

    def __get_messages(self, node: WorkflowNodeRequest):
        prompt_template = ChatPromptTemplate(
            [SystemMessage(content=node.prompt or ""), MessagesPlaceholder("msgs")]
        )
        return prompt_template.invoke(
            {
                "msgs": [HumanMessage(content=node.message or "")],
            }
        )
