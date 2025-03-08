from ai.exceptions.exception import LLmException
from ai.services import LLmService


class BlogWorkflow:

    def __init__(self, llm: str):
        self.llm_model = LLmService(llm=llm).get_llm()
        if not self.llm_model:
            raise LLmException(detail="LLM not selected")
