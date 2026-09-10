from memory.state import TravelState
from core.llm import llm
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)
from prompts.itinerary import ITINERARY_AGENT_PROMPT


def itinerary_agent(state: TravelState):
    prompt = ITINERARY_AGENT_PROMPT.format(
        user_query=state["user_query"],
        flight_results=state["flight_results"],
        hotel_results=state["hotel_results"]
    )

    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner."),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }