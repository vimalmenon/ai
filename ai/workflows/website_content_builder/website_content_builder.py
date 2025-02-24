from typing import Annotated

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from ai.llms.ollama import ollama_llm
from ai.utilities import get_data_path, read_from_file
from ai.workflows.base_builder.base_builder import BaseBuilder


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


class WebsiteContentBuilder(BaseBuilder):
    graph_builder: StateGraph

    def __init__(self):
        self.graph_builder = StateGraph(State)

    def invoke(self):
        print(self._load_data())

    def _get_topic(self):
        pass

    def _load_data(self) -> str:
        return read_from_file(get_data_path("website/data.txt"))
