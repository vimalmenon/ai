from ai.agents.simple_agents import agent_executor
from langchain_core.messages import HumanMessage


def run():
    config = {"configurable": {"thread_id": "abc123"}}
    messages = []
    print("Hello!! My name is Elara, How can i help you today?")
    while user_input := input("You: "):
        if user_input.lower() == "bye":
            print("Elara: Bye! Have a nice day!")
            break
        for step in agent_executor.stream(
            {"messages": messages.append(HumanMessage(content=user_input))},
            config,
            stream_mode="values",
        ):
            step["messages"][-1].pretty_print()
