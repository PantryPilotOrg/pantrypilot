from app.agent.agent import agent
from app.agent.tracing import clear_steps, get_steps


def run_agent(prompt: str) -> dict:
    """
    Run PantryPilot for a user prompt and return the final response
    together with the recorded LLM execution steps.
    """
    clear_steps()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        }
    )

    final_response = result["messages"][-1].content

    return {
        "response": final_response,
        "steps": get_steps(),
    }