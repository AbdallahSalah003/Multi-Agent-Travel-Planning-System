from typing import TypedDict, Annotated, Any
import operator
from langchain_core.messages import AnyMessage


class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str

    # Supervisor + guardrails 
    guardrail_allowed: bool
    guardrail_reason: str
    selected_agents: list[str]
    trip_constraints: dict[str, Any] # destination, duration, ...etc
    supervisor_reasoning: str

    # Original specialists results
    flight_results: str
    hotel_results: str
    itinerary: str
    weather_results: str

    # Budget + HITL 
    budget_results: str
    approval_request: str
    approved: bool
    human_feedback: str
    final_response: str

    llm_calls: int

