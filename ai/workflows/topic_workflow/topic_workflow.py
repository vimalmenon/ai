from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import create_react_agent

from ai.exceptions.exceptions import LLmException
from ai.model.llm import LLMs
from ai.services import LlmService
from ai.utilities import generate_uuid
from ai.workflows.base_builder.base_builder import State


class TopicWorkflow:
    wf_id = "9454830b-6daf-47f7-8fca-13d966660cf1"

    def __init__(self, llm: LLMs):
        self.id = generate_uuid()
        self.llm_model = LlmService().get_llm(llm=llm)
        self.graph_builder = StateGraph(State)
        self.messages: list = []
        if not self.llm_model:
            raise LLmException(detail="LLM not selected")

    def execute(self):
        agents = self._create_connect_and_compile_nodes()
        for response in agents.stream(
            {"messages": self.messages + [HumanMessage("Topic is python")]},
            stream_mode="values",
        ):
            print(response)

    def _create_connect_and_compile_nodes(self):
        topic_writer = self._initialize_topic_writer_agent()
        self.graph_builder.add_node("WRITER", topic_writer)
        self.graph_builder.add_edge(START, "WRITER")
        self.graph_builder.add_edge("WRITER", END)
        return self.graph_builder.compile()

    def _initialize_topic_writer_agent(self):
        return create_react_agent(
            model=self.llm_model,
            tools=[],
            name="topic_writer",
            prompt=(
                "You have to come up with 10 titles for the blogs based on topic."
                "Give the output as a list."
                "Topic should be innovative and interesting"
            ),
        )
