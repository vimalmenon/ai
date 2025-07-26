from logging import getLogger

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent

from ai.managers.ai_message_manager.ai_message_manager import AiMessageManager
from ai.model import AiMessage, WorkflowNodeRequest
from ai.model.enums import WorkflowType
from ai.services.llm_service.llm_service import LlmService
from ai.services.tool_service.tool_service import ToolService
from ai.utilities import generate_uuid

logger = getLogger(__name__)


class LLMExecuteService:

    def execute(self, node: WorkflowNodeRequest) -> None:
        if node.type == WorkflowType.LLM:
            self.execute_llm(node)
        else:
            self.execute_agent(node)

    def execute_agent(self, node: WorkflowNodeRequest) -> None:
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
        for result in agent_llm.stream(prompt_messages):
            logger.warning(result)
            AiMessageManager().save_data(
                AiMessage(id=generate_uuid(), content=result["content"])
            )

    def execute_llm(self, node: WorkflowNodeRequest) -> None:
        llm = LlmService().get_llm(
            llm=node.llm, structured_output=node.structured_output
        )
        prompt_messages = self.__get_messages(node)
        result = llm.invoke(prompt_messages)
        logger.warning(result)
        AiMessageManager().save_data(
            AiMessage(
                id=generate_uuid(), content=result.content, model_name=result.model_name
            )
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
