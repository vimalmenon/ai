from uuid import uuid4

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ai.agents.simple_agents import agent_executor


def run():
    config = {"configurable": {"thread_id": str(uuid4())}}
    messages = [
        SystemMessage(content="Your name is Elara, You are helpful AI assistant")
    ]
    print("Hello!! My name is Elara, How can i help you today?")
    while user_input := input("You: "):
        if user_input.lower() == "bye":
            print("Elara: Bye! Have a nice day!")
            break
        messages.append(HumanMessage(content=user_input))
        for step in agent_executor.stream(
            {"messages": messages},
            config,
            stream_mode="values",
        ):
            messages.append(AIMessage(content=step["messages"][-1].content))
            step["messages"][-1].pretty_print()
