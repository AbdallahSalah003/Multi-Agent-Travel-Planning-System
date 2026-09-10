import uuid
from langgraph.graph import StateGraph, END
from langchain_core.messages import (HumanMessage)
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from memory.state import TravelState
from agents.flight import flight_agent
from agents.hotel import hotel_agent
from agents.weather import weather_agent
from agents.final_agent import final_agent
from agents.itinerary import itinerary_agent
from core.database import get_db_conn

FLIGHT_AGENT="flight_agent"
HOTEL_AGENT="hotel_agent"
WEATHER_AGENT="weather_agent"
ITINERARY_AGENT="itinerary_agent"
FINAL_AGENT="final_agent"

async def build_graph():

    builder = StateGraph(TravelState)
    builder.add_node(FLIGHT_AGENT, flight_agent)
    builder.add_node(HOTEL_AGENT, hotel_agent)
    builder.add_node(WEATHER_AGENT, weather_agent)
    builder.add_node(ITINERARY_AGENT, itinerary_agent)
    builder.add_node(FINAL_AGENT, final_agent)

    builder.set_entry_point(FLIGHT_AGENT)
    builder.add_edge(FLIGHT_AGENT, HOTEL_AGENT)
    builder.add_edge(HOTEL_AGENT, WEATHER_AGENT)
    builder.add_edge(WEATHER_AGENT, ITINERARY_AGENT)
    builder.add_edge(ITINERARY_AGENT, FINAL_AGENT)
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

    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = await graph.ainvoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "weather_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )
    final_answer = result["messages"][-1].content

    return {
        "thread_id": thread_id,
        "answer": final_answer,
        "flight_results": result.get("flight_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "weather_results": result.get("weather_results", ""),
        "itinerary": result.get("itinerary", ""),
        "llm_calls": result.get("llm_calls", 0) 
    }



