import uuid
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from langchain_core.messages import (HumanMessage)
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from memory.state import TravelState
from structured_outputs.supervisor import TripConstraints
from agents.guardrail import guardrail_agent
from agents.supervisor import supervisor_agent
from agents.flight import flight_agent
from agents.hotel import hotel_agent
from agents.weather import weather_agent
from agents.budget import budget_agent
from agents.final_agent import final_agent
from agents.itinerary import itinerary_agent
from agents.hitl import human_approval_agent
from core.database import get_db_conn
from utils.agents import AGENT_ORDER, KNOWN_AGENTS
from utils.fastapi_facing import serialize_result

GUARDRAIL_AGENT="guardrail_agent"
SUPERVISOR_AGENT="supervisor_agent"
FLIGHT_AGENT="flight_agent"
HOTEL_AGENT="hotel_agent"
WEATHER_AGENT="weather_agent"
BUDGET_AGENT="budget_agent"
ITINERARY_AGENT="itinerary_agent"
HUMAN_APPROVAL_AGENT="human_approval_agent"
FINAL_AGENT="final_agent"


async def build_graph():
    def route_from_guardrail_agent(state: TravelState) -> str:
        if not state["guardrail_allowed"]:
            return END
        return SUPERVISOR_AGENT

    def route_from_supervisor(state: TravelState) -> str:
        selected_agents = state["selected_agents"]
        return selected_agents[0] if len(selected_agents)>0 else ITINERARY_AGENT

    def route_from_specialist_agent(current_agent: str):
        def route(state: TravelState) -> str:
            index = AGENT_ORDER.index(current_agent)
            for next_agent in AGENT_ORDER[index + 1:]:
                if next_agent in state["selected_agents"]:
                    return next_agent
            return ITINERARY_AGENT

        return route

    ROUTE_MAP = {
        END: END,
        GUARDRAIL_AGENT: GUARDRAIL_AGENT,
        SUPERVISOR_AGENT: SUPERVISOR_AGENT,
        FLIGHT_AGENT: FLIGHT_AGENT,
        HOTEL_AGENT: HOTEL_AGENT,
        WEATHER_AGENT: WEATHER_AGENT,
        BUDGET_AGENT: BUDGET_AGENT,
        ITINERARY_AGENT: ITINERARY_AGENT,
        FINAL_AGENT: FINAL_AGENT
    }

    builder = StateGraph(TravelState)
    builder.add_node(GUARDRAIL_AGENT, guardrail_agent)
    builder.add_node(SUPERVISOR_AGENT, supervisor_agent)
    builder.add_node(FLIGHT_AGENT, flight_agent)
    builder.add_node(HOTEL_AGENT, hotel_agent)
    builder.add_node(WEATHER_AGENT, weather_agent)
    builder.add_node(BUDGET_AGENT, budget_agent)
    builder.add_node(ITINERARY_AGENT, itinerary_agent)
    builder.add_node(HUMAN_APPROVAL_AGENT, human_approval_agent)
    builder.add_node(FINAL_AGENT, final_agent)

    builder.set_entry_point(GUARDRAIL_AGENT)
    builder.add_conditional_edges(
        GUARDRAIL_AGENT, 
        route_from_guardrail_agent, 
        ROUTE_MAP
    )
    builder.add_conditional_edges(
        SUPERVISOR_AGENT, 
        route_from_supervisor, 
        ROUTE_MAP
    )
    builder.add_conditional_edges(
        FLIGHT_AGENT, 
        route_from_specialist_agent(FLIGHT_AGENT), 
        ROUTE_MAP
    )
    builder.add_conditional_edges(
        HOTEL_AGENT,
        route_from_specialist_agent(HOTEL_AGENT),
        ROUTE_MAP 
    )
    builder.add_conditional_edges(
        WEATHER_AGENT,
        route_from_specialist_agent(WEATHER_AGENT),
        ROUTE_MAP 
    )
    builder.add_conditional_edges(
        BUDGET_AGENT,
        route_from_specialist_agent(BUDGET_AGENT),
        ROUTE_MAP
    )
    builder.add_edge(ITINERARY_AGENT, HUMAN_APPROVAL_AGENT)
    builder.add_edge(HUMAN_APPROVAL_AGENT, FINAL_AGENT)
    builder.add_edge(FINAL_AGENT, END)

    conn = await get_db_conn()
    checkpointer = AsyncPostgresSaver(conn=conn)
    await checkpointer.setup()

    graph = builder.compile(checkpointer=checkpointer)

    return graph, conn


async def run_travel_planner(
    graph,
    user_input: str, 
    thread_id: str | None = None,
):
    """Start a new travel-planning run and pause at human approval""" 

    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = await graph.ainvoke(
        {
            "messages": [HumanMessage(content=user_input)],
            "user_query": user_input,
            "guardrail_allowed": True,
            "guardrail_reason": "",
            "selected_agents": [],
            "trip_constraints": TripConstraints(),
            "supervisor_reasoning": "",
            "flight_results": "",
            "hotel_results": "",
            "weather_results": "",
            "budget_results": "",
            "itinerary": "",
            "approval_request": "",
            "approved": False,
            "human_feedback": "",
            "final_response": "",
            "llm_calls": 0,
        },
        config=config
    )

    return serialize_result(result=result, thread_id=thread_id)


async def resume_travel_agent(
    graph,
    thread_id: str,
    approved: bool,
    feedback: str = ""
):
    """Resume the paused Langgrph thread after human review"""
    if not thread_id:
        raise ValueError("thread_id is required to resume a travel paln.")

    config = {"configurable": {"thread_id": thread_id}}
    result = await graph.ainvoke(
        Command(
            resume={
                "approved": approved,
                "feedback": feedback.strip(),
            }
        ),
        config=config
    )

    return serialize_result(result=result, thread_id=thread_id)
