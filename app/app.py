from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.agent.runner import run_agent
from app.services.scheduler_service import run_days

class ExecuteRequest(BaseModel):
    prompt: str

class SimulationRequest(BaseModel):
    prompt: str
    start_day: int
    end_day: int

app = FastAPI()
STATIC_DIR = Path(__file__).resolve().parent / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/api/team_info")
def get_team_info():
    return {
        "group_batch_order_number": "1_3",
        "team_name": "PantryPilot",
        "students": [
            {
                "name": "Chana Gutenmacher",
                "email": "chana4@gmail.com"
            },
            {
                "name": "Ayla Livney",
                "email": "aylalivney@gmail.com"
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

@app.get("/api/model_architecture")
def get_model_architecture():
    return FileResponse(
        STATIC_DIR / "model_architecture.png",
        media_type="image/png"
    )

@app.get("/")
def get_gui():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/api/execute")
def execute(request: ExecuteRequest):
    try:
        result = run_agent(request.prompt)

        return {
            "status": "ok",
            "error": None,
            "response": result["response"],
            "steps": result["steps"]
        }

    except Exception as error:
        return {
            "status": "error",
            "error": str(error),
            "response": None,
            "steps": []
        }

@app.post("/api/simulate")
def simulate(request: SimulationRequest):
    try:
        results = run_days(
            request.start_day,
            request.end_day,
            request.prompt,
        )

        return {
            "status": "ok",
            "error": None,
            "results": results,
        }

    except Exception as error:
        return {
            "status": "error",
            "error": str(error),
            "results": [],
        }        