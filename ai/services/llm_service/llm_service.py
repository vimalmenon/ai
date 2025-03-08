from typing import Any

from ai.llms import deepseek_llm, google_llm


class LLmService:
    item: Any | None = None

    def __init__(self, llm: str):
        if llm == "Deepseek":
            self.item = deepseek_llm
        elif llm == "Google":
            self.item = google_llm

    def get_llm(self) -> Any | None:
        return self.item
