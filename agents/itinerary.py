from memory.state import TravelState
from services.llm import instrumented_llm
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)
from prompts.itinerary import ITINERARY_AGENT_PROMPT
from prompts.approval import REQUEST_APPROVAL


async def itinerary_agent(state: TravelState):
    prompt = ITINERARY_AGENT_PROMPT.format(
        user_query=state["user_query"],
        trip_constraints=state["trip_constraints"],
        flight_results=state["flight_results"],
        hotel_results=state["hotel_results"],
        weather_results=state["weather_results"],
        budget_results=state["budget_results"]
    )
    llm = instrumented_llm.get_llm()
    response = await llm.ainvoke([
        SystemMessage(content="You are an expert travel planner."),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "approval_request": REQUEST_APPROVAL,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }