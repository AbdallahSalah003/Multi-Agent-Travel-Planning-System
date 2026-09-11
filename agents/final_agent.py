from memory.state import TravelState
from services.llm import instrumented_llm
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)
from prompts.final_agent import FINAL_AGENT_PROMPT

async def final_agent(state: TravelState):
    if state.get("approved", False):
        review_instruction = (
            "The user approved the draft. Preserve its decisions while polishing it."
        )
    else:
        review_instruction = f"""
            The user requested a revision. Apply this feedback carefully:
            {state.get('human_feedback', '') or 'Improve the draft before finalizing it.'}
        """

    prompt = FINAL_AGENT_PROMPT.format(
        review_instructions=review_instruction,
        user_query=state["user_query"],
        trip_constraints=state["trip_constraints"],
        flight_results=state["flight_results"],
        hotel_results=state["hotel_results"],
        weather_results=state["weather_results"],
        budget_results=state["budget_results"],
        itinerary=state["itinerary"]
    )
    llm = instrumented_llm.get_llm()
    response = await llm.ainvoke([
        SystemMessage(content="You are a professional AI travel booking assistant."),
        HumanMessage(content=prompt)
    ])

    return {
        "final_response": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
