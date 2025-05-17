from langchain_core.tools import tool


@tool
def text_to_speech(text: str):
    """
    Use this tool to convert text to speech
    Use this tool only on request.
    """
    print(text)
