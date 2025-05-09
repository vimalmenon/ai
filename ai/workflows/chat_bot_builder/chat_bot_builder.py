from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, START, StateGraph

from ai.services.llm_service.ollama import ollama_llm
from ai.workflows.base_builder.base_builder import BaseBuilder, State


class ChatBotBuilder(BaseBuilder):
    graph_builder: StateGraph
    messages: list = []

    def __init__(self):
        self.graph_builder = StateGraph(State)
        self.messages = []

    def _prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Your name is Elara (Ela), you are helpful AI assistant to Vimal Menon.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

    def _create_chatbot_agent(self, state):
        prompt = self._prompt()
        agents = prompt | ollama_llm
        response = agents.invoke(
            {
                "messages": state["messages"],
            }
        )
        return {"messages": [AIMessage(content=response.content)]}

    def _connect_node_and_edge_and_compile(self):
        self.graph_builder.add_node("CHATBOT", self._create_chatbot_agent)
        self.graph_builder.add_edge(START, "CHATBOT")
        self.graph_builder.add_edge("CHATBOT", END)
        return self.graph_builder.compile()

    def _stream_message(self, app, user_input: str):
        return app.stream(
            {"messages": self.messages + [HumanMessage(content=user_input)]},
            stream_mode="values",
        )

    def _store_messages(self, events):
        for event in events:
            self.messages.append(AIMessage(content=event["messages"][-1].content))
            event["messages"][-1].pretty_print()

    def invoke(self):
        app = self._connect_node_and_edge_and_compile()
        print("Hello!! My name is Elara, How can i help you today?")
        while user_input := input("You: "):
            if user_input.lower() == "bye":
                print("Elara: Bye! Have a nice day!")
                break
            events = self._stream_message(app, user_input)
            self._store_messages(events)
