from langchain_core.tools import tool


@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together. always use this tool for multiplication."""
    return first_int * second_int
