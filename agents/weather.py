from langchain_core.messages import AIMessage
from memory.state import TravelState
from utils.prompt_extract import extract_destination
from mcp_pkg.client import weather_mcp_search, forecast_mcp_search


async def weather_agent(state: TravelState):

    city = await extract_destination(state["user_query"])

    weather_data = await weather_mcp_search(city)

    forecast_data = await forecast_mcp_search(city)

    return {
        "weather_results": f"""
        Current Weather:
        {weather_data}

        Forecast:
        {forecast_data}
        """,
        "messages": [
            AIMessage(
                content="Weather information fetched"
            )
        ]
    }