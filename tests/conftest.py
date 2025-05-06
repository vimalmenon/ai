import os

def setup_env() -> None:
    """
    Set up the environment for testing.
    """
    os.environ["SUPPORTED_LLM"] = "DEEPSEEK"