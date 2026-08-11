from fastapi import FastAPI
from pydantic import BaseModel

class ExecuteRequest(BaseModel):
    prompt: str

app = FastAPI()


@app.get("/api/team_info")
def get_team_info():
    return {
        "group_batch_order_number": "TODO",
        "team_name": "PantryPilot",
        "students": [
            {
                "name": "Chana Gutenmacher",
                "email": "TODO"
            },
            {
                "name": "Ayla Livney",
                "email": "TODO"
            }
        ]
    }


@app.get("/api/agent_info")
def get_agent_info():
    return {
        "description": (
            "PantryPilot is an autonomous household inventory and grocery "
            "purchasing agent."
        ),
        "purpose": (
            "Help manage household stock, reduce food waste, avoid shortages, "
            "and make cost-aware purchasing decisions."
        ),
        "prompt_template": {
            "template": "Manage my kitchen for the current simulated day."
        },
        "prompt_examples": [
            {
                "prompt": "Manage my kitchen today.",
                "full_response": "TODO - replace with a real agent response.",
                "steps": []
            }
        ]
    }

@app.post("/api/execute")
def execute(request: ExecuteRequest):
    try:
        return {
            "status": "ok",
            "error": None,
            "response": f"Received prompt: {request.prompt}",
            "steps": []
        }

    except Exception as error:
        return {
            "status": "error",
            "error": str(error),
            "response": None,
            "steps": []
        }