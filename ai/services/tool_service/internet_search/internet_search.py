from langchain_core.tools import Tool, tool
from langchain_google_community import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper(k=1)


def top5_results(query):
    return search.results(query, 5)


search_tool = Tool(
    name="I'm Feeling Lucky",
    description="Search Google for recent results.",
    func=top5_results,
)


@tool("internet_search")
def internet_search(query: str) -> list[dict]:
    """Search Google for recent results."""
    return search_tool.run(query)
