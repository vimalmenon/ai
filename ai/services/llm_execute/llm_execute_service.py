from logging import getLogger

from langgraph.prebuilt import create_react_agent

from ai.model import (
    WorkflowNodeRequest,
)
from ai.services.llm_service.llm_service import LLmService
from ai.services.tool_service.tool_service import ToolService

logger = getLogger(__name__)


class LLMExecuteService:

    def execute(self, node: WorkflowNodeRequest):
        agent_llm = create_react_agent(
            model=LLmService(llm=node.llm).get_llm(),
            tools=[ToolService().get_tool_func(tool) for tool in node.tools],
            name=node.name,
            prompt="You are a helpful assistant",
        )
        result = agent_llm.invoke(
            {"messages": [{"role": "user", "content": node.prompt}]}
        )
        logger.info(result)
        return result
