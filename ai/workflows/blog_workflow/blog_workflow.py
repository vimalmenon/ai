from langgraph.prebuilt import create_react_agent

from ai.exceptions.exception import LLmException
from ai.services import LLmService


class BlogWorkflow:

    def __init__(self, llm: str):
        self.llm_model = LLmService(llm=llm).get_llm()
        if not self.llm_model:
            raise LLmException(detail="LLM not selected")

    def _initialize_resume_critique_agent(self):
        return create_react_agent(
            model=self.llm_model,
            tools=[],
            name="resume_critique",
            prompt="You have to critique resume and provide detailed feedback to improve resume",
        )
