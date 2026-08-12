from collections.abc import Callable

from langchain.agents.middleware import (
    ModelRequest,
    ModelResponse,
    wrap_model_call,
)


steps: list[dict] = []


@wrap_model_call
def trace_model_call(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """
    Record each LLM call made by the agent.

    The trace stores the model input and output in the format required
    by the project API.
    """
    response = handler(request)

    steps.append(
        {
            "module": "pantrypilot_agent",
            "prompt": {
                "messages": [
                    message.model_dump()
                    for message in request.messages
                ]
            },
            "response": {
                "messages": [
                    message.model_dump()
                    for message in response.result
                ]
            },
        }
    )

    return response


def clear_steps() -> None:
    """Clear the trace before starting a new agent execution."""
    steps.clear()


def get_steps() -> list[dict]:
    """Return the recorded LLM-call trace."""
    return steps.copy()