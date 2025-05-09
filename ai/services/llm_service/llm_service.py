from langchain_core.language_models.base import LanguageModelLike

from ai.config import env
from ai.llms import deepseek_llm, google_llm, ollama_llm
from ai.model.llm import LLMs


class LLmService:
    item: LanguageModelLike

    def __init__(self, llm: LLMs | None = LLMs.DEEPSEEK) -> None:
        if llm == LLMs.DEEPSEEK:
            self.item = deepseek_llm
        elif llm == LLMs.GOOGLE:
            self.item = google_llm
        elif llm == LLMs.OLLAMA:
            self.item = ollama_llm

    def get_llm(self) -> LanguageModelLike:
        return self.item


class ListLLMServices:
    def list_llm_details(self):
        return [
            {
                "name": LLMs.DEEPSEEK,
                "model": "deepseek-chat",
                "supported": LLMs.DEEPSEEK.value in env.supported_llm,
            },
            {
                "name": LLMs.GOOGLE,
                "model": "gemini-1.5-pro",
                "supported": LLMs.GOOGLE.value in env.supported_llm,
            },
            {
                "name": LLMs.OLLAMA,
                "model": "mistral",
                "supported": LLMs.OLLAMA.value in env.supported_llm,
            },
        ]


class CreateLLMServices:
    pass
