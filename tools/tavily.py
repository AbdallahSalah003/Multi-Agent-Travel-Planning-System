import os
from tavily import TavilyClient
from dotenv import load_dotenv


load_dotenv()


client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def tavily_search(query: str) -> str:
    """
    Search using the tavily api and the input query over the internt.

    Params:
        query: User input query
    
    Returns:
        result: A string with the search results.
    """
    response = client.search(
        query=query,
        max_results=5
    )
    results = []

    for index, result in enumerate(response["results"], 1):
        title = result.get("title", "UNK")
        url = result.get("url", "")
        body = result.get("content", "").strip()

        if len(body) > 300:
            body = body[:300].rsplit(" ", 1)[0] + "..."

        results.append(f"{index}. **{title}**\n  {url}\n {body}")

    return "\n\n".join(results)