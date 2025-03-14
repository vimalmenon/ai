from langchain_core.tools import tool


@tool
def save_to_s3(item: str):
    """
    Use this tool to Upload the item to S3 bucket
    Use this tool only on request.
    """
    print(item)
