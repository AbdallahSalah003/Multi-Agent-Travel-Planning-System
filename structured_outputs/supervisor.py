from typing import List, Literal
from pydantic import BaseModel, Field


AgentName = Literal[
    "flight_agent",
    "hotel_agent",
    "weather_agent",
    "budget_agent",
    "itinerary_agent",
]


class TripConstraints(BaseModel):
    destination: str = Field(default="",description="The trip destination")
    origin: str = Field(default="",description="The trip origin")
    duration: str = Field(default="",description="The trip duration")
    budget: str = Field(default="",description="The user's trip budget")
    travel_style: str = Field(default="",description="The user's preferred travel style")
    special_preferences: List[str] = Field(
        default_factory=list,
        description="Any special preferences or requirements",
    )


class SupervisorResponse(BaseModel):
    selected_agents: List[AgentName] = Field(
        description="Agents that should be called for this trip"
    )
    trip_constraints: TripConstraints
    reasoning: str = Field(
        description="Explanation for why these agents were selected"
    )