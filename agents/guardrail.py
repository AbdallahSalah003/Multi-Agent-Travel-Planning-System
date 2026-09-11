from memory.state import TravelState
from services.llm import instrumented_llm
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from prompts.guardrail import GUARDRAIL_PROMPT
from structured_outputs.guardrail import GuardrailResponse
from services.pii_cleaner import clean_pii

async def guardrail_agent(state: TravelState):
    user_query = state["user_query"]

    cleaned_query = clean_pii(user_query)

    model = instrumented_llm.get_llm_with_structured_output(
        GuardrailResponse
    )

    messages = [
        SystemMessage(
            content=GUARDRAIL_PROMPT.format(query=cleaned_query)
        ),
        HumanMessage(content=cleaned_query),
    ]

    response: GuardrailResponse = await model.ainvoke(messages)

    return {
        "user_query": cleaned_query,
        "messages": [
            AIMessage(
                content="Guardrail Agent Finished."
            )
        ],
        "guardrail_allowed": response.allowed,
        "guardrail_reason": response.reason,
        "llm_calls": state.get("llm_calls", 0) + 1
    }