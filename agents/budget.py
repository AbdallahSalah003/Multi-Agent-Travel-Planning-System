from memory.state import TravelState
from services.llm import instrumented_llm
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from prompts.budget import BUDGET_AGENT_PROMPT

async def budget_agent(state: TravelState):
    model = instrumented_llm.get_llm()
    response = await model.ainvoke(
        [
            SystemMessage(content="You are a practical travel budget analyst."),
            HumanMessage(
                content = BUDGET_AGENT_PROMPT.format(
                    user_query=state["user_query"],
                    trip_constraints=state["trip_constraints"],
                    flight_results=state["flight_results"],
                    hotel_results=state["hotel_results"],
                    weather_results=state["weather_results"]
                )
            ),
        ]
    )

    return {
        "budget_results": response.content,
        "messages": [AIMessage(content="Budget assessment generated.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }