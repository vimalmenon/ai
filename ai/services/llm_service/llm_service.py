from typing import Any

from ai.enum import LLMs
from ai.llms import deepseek_llm, google_llm, ollama_llm


class LLmService:
    item: Any | None = None

    def __init__(self, llm: LLMs):
        if llm == LLMs.DEEPSEEK:
            self.item = deepseek_llm
        elif llm == LLMs.GOOGLE:
            self.item = google_llm
        elif llm == LLMs.OLLAMA:
            self.item = ollama_llm

    def get_llm(self) -> Any | None:
        return self.item
