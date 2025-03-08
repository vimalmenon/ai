from ai.services import LLmService


class BlogWorkflow:

    def __init__(self, llm: str):
        self.llm_model = LLmService(llm=llm).get_llm()
