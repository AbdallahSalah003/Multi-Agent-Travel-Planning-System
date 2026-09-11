from memory.state import TravelState
from services.llm import instrumented_llm
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from prompts.supervisor import SUPERVISOR_PROMPT, SUPERVISOR_SYS_PROMPT
from structured_outputs.supervisor import SupervisorResponse, TripConstraints
from utils.agents import AGENT_ORDER, KNOWN_AGENTS

async def supervisor_agent(state: TravelState):
    try: 
        model = instrumented_llm.get_llm_with_structured_output(SupervisorResponse)
        prompt = SUPERVISOR_PROMPT.format(
            query=state["user_query"]
        )
        response: SupervisorResponse = await model.ainvoke(
            [
                SystemMessage(content=SUPERVISOR_SYS_PROMPT),
                HumanMessage(content=prompt)
            ]
        )
        requested_agents = response.selected_agents 
        selected_agents_in_order = [
            name for name in AGENT_ORDER
            if name  in requested_agents and name in KNOWN_AGENTS
        ]
        trip_constraints: TripConstraints = response.trip_constraints
        reasoning = response.reasoning
    except Exception as e:
        # Fallback to full travel workflow
        selected_agents_in_order = AGENT_ORDER.copy()
        trip_constraints = TripConstraints()
        reasoning = (
            "Supervisor parsing failed, so the original full travel workflow "
            "was selected as a safe fallback."
        )
    return {
        "selected_agents": selected_agents_in_order,
        "trip_constraints": trip_constraints,
        "supervisor_reasoning": reasoning,
        "messages": [AIMessage(content="Supervisor created the agent plan.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
