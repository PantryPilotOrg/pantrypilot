from collections.abc import Callable

from langchain.agents.middleware import (
    ModelRequest,
    ModelResponse,
    wrap_model_call,
)


steps: list[dict] = []


def _serialize_message(message) -> dict:
    """
    Convert a LangChain message to a compact trace representation.
    Keep only information relevant to understanding the agent's behavior.
    """
    serialized = {
        "type": message.type,
        "content": message.content,
    }

    if getattr(message, "name", None):
        serialized["name"] = message.name

    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        serialized["tool_calls"] = [
            {
                "name": tool_call.get("name"),
                "args": tool_call.get("args"),
            }
            for tool_call in tool_calls
        ]

    return serialized


@wrap_model_call
def trace_model_call(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """
    Record each LLM call made by the agent.

    The trace stores only the model input and output information needed
    to understand the agent's decisions.
    """
    response = handler(request)

    steps.append(
        {
            "module": "pantrypilot_agent",
            "prompt": {
                "messages": [
                    _serialize_message(message)
                    for message in request.messages
                ]
            },
            "response": {
                "messages": [
                    _serialize_message(message)
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