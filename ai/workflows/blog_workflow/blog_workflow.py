from langgraph.prebuilt import create_react_agent

from ai.exceptions.exceptions import LLmException
from ai.model.llm import LLMs
from ai.services import LlmService
from ai.utilities import generate_uuid


class BlogWorkflow:
    wf_id = "18aad31b-ef41-4853-a97a-17fd8647574c"

    def __init__(self, llm: LLMs):
        self.id = generate_uuid()
        self.llm_model = LlmService().get_llm(llm=llm)
        if not self.llm_model:
            raise LLmException(detail="LLM not selected")

    def _initialize_resume_critique_agent(self):
        return create_react_agent(
            model=self.llm_model,
            tools=[],
            name="resume_critique",
            prompt="You have to critique resume and provide detailed feedback to improve resume",
        )
