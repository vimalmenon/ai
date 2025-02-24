from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, START, StateGraph

from ai.llms.ollama import ollama_llm
from ai.utilities import get_data_path, read_from_file
from ai.workflows.base_builder.base_builder import BaseBuilder, State


class WebsiteContentBuilder(BaseBuilder):
    graph_builder: StateGraph

    def __init__(self):
        self.graph_builder = StateGraph(State)

    def invoke(self):
        app = self._connect_node_and_edge_and_compile()
        events = app.stream(
            {"messages": [HumanMessage(content="Generate a About Me page")]},
            stream_mode="values",
        )
        self.pretty_print_response(events)

    def _connect_node_and_edge_and_compile(self):
        self.graph_builder.add_node("CONTENTS", self._content_agent_node)
        self.graph_builder.add_edge(START, "CONTENTS")
        self.graph_builder.add_edge("CONTENTS", END)
        return self.graph_builder.compile()

    def _content_agent_node(self, state):
        prompts = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a content writer for blogs and websites."
                    "You have to generate detailed page based on below content.\n"
                    "Page title : {page_title}\n"
                    "Page content: {page_content}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        agents = prompts | ollama_llm
        response = agents.invoke(
            {
                "page_title": "About Me",
                "page_content": self._load_data(),
                "messages": state["messages"],
            }
        )
        return {"messages": [AIMessage(content=response.content)]}

    def _load_data(self) -> str:
        return read_from_file(get_data_path("website/data.txt"))
