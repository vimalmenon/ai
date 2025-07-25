from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from ai.config import env
from ai.model.enums import LLMs, StructuredOutputType
from ai.services.service.structured_output_service import StructuredOutputService


class LlmService:

    def get_llm(
        self,
        llm: LLMs | None = LLMs.DEEPSEEK,
        structured_output: StructuredOutputType | None = None,
    ):
        output_cls = StructuredOutputService().get_structured_output(structured_output)
        if llm == LLMs.DEEPSEEK:
            deepseek_llm = self.__deepseek_llm()
            # deepseek_llm.with_structured_output(output_cls)
            return deepseek_llm
        elif llm == LLMs.GOOGLE:
            google_llm = self.__google_llm()
            google_llm.with_structured_output(output_cls)
            return google_llm
        elif llm == LLMs.OLLAMA:
            ollama_llm = self.__ollama_llm()
            ollama_llm.with_structured_output(output_cls)
            return ollama_llm
        elif llm == LLMs.OpenAI:
            openai_llm = self.__openai_llm()
            openai_llm.with_structured_output(output_cls)
            return openai_llm

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
            {
                "name": LLMs.OpenAI,
                "model": "gpt-4o",
                "supported": LLMs.OpenAI.value in env.supported_llm,
            },
        ]

    def __deepseek_llm(self):
        return ChatDeepSeek(
            model="deepseek-chat",
            temperature=env.temperature,
            max_tokens=None,
        )

    def __google_llm(self):
        return ChatGoogleGenerativeAI(
            temperature=env.temperature, model="gemini-1.5-pro"
        )

    def __openai_llm(self):
        return ChatOpenAI(
            model="gpt-4o",
            temperature=env.temperature,
        )

    def __ollama_llm(self):
        return init_chat_model(
            "mistral", model_provider="ollama", temperature=env.temperature
        )
