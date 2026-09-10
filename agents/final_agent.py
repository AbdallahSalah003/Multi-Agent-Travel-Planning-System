from memory.state import TravelState
from core.llm import llm
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)
from prompts.final_agent import FINAL_AGENT_PROMPT

def final_agent(state: TravelState):
    prompt = FINAL_AGENT_PROMPT.format(
        user_query=state["user_query"],
        flight_results=state["flight_results"],
        hotel_results=state["hotel_results"],
        weather_results=state["weather_results"],
        itinerary=state["itinerary"]
    )
    response = llm.invoke([
        SystemMessage(content="You are a professional AI travel booking assistant."),
        HumanMessage(content=prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
