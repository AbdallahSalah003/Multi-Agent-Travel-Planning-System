from langchain.agents import AgentState
from langchain.agents.middleware import PIIMiddleware
from langchain_core.messages import HumanMessage
from langgraph.runtime import Runtime

def clean_pii(text: str) -> str:
    pii_middleware = [
        PIIMiddleware(
            "email",
            strategy="redact",
        ),
        PIIMiddleware(
            "mac_address",
            strategy="redact",
        ),
        PIIMiddleware(
            "credit_card",
            strategy="mask",
        ),
    ]

    middleware_state = AgentState(
        messages=[
            HumanMessage(content=text)
        ]
    )

    runtime = Runtime()

    for middleware in pii_middleware:
        result = middleware.before_model(
            middleware_state,
            runtime,
        )

        if result:
            middleware_state = AgentState(
                messages=result["messages"]
            )

    return middleware_state["messages"][0].content