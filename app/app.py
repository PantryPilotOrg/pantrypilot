from pathlib import Path
import json
import re

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
    examples_file = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "agent_info_examples.json"
    )

    with examples_file.open(encoding="utf-8-sig") as file:
        prompt_examples = json.load(file)

    return {
        "description": (
            "PantryPilot is an autonomous household shopping agent that "
            "observes changing household needs, compares purchase options, "
            "and decides what to buy, when to order, and when to wait."
        ),
        "purpose": (
            "Reduce the mental load of recurring household shopping while "
            "preventing shortages and unnecessary purchases and considering "
            "budget, expiry, upcoming events, and delivery constraints."
        ),
        "prompt_template": {
            "template": "Manage my household for day {day}."
        },
        "prompt_examples": prompt_examples,
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
        prompt = request.prompt

        range_match = re.search(
            r" from day (\d+) through day (\d+)",
            prompt,
            re.IGNORECASE,
        )

        if range_match:
            start_day = int(range_match.group(1))
            end_day = int(range_match.group(2))

            if not 1 <= start_day <= 7 or not 1 <= end_day <= 7:
                raise ValueError("Days must be between 1 and 7.")

            if start_day > end_day:
                raise ValueError("Start day cannot be after end day.")

            base_prompt = re.sub(
                r"manage the household from day \d+ through day \d+\.",
                "",
                prompt,
                flags=re.IGNORECASE,
            ).strip().rstrip(" .")

            results = run_days(
                start_day,
                end_day,
                base_prompt,
            )

            responses = []
            all_steps = []

            for day_result in results:
                day = day_result.get("simulation_day")
                day_response = day_result.get("response", "")

                responses.append(
                    f"DAY {day}\n{day_response}"
                )

                all_steps.extend(day_result.get("steps", []))

            return {
                "status": "ok",
                "error": None,
                "response": "\n\n".join(responses),
                "steps": all_steps,
            }

        single_day_match = re.search(
            r"day (\d+)",
            prompt,
            re.IGNORECASE,
        )

        if single_day_match:
            day = int(single_day_match.group(1))

            if not 1 <= day <= 7:
                raise ValueError("Day must be between 1 and 7.")

            base_prompt = re.sub(
                r"manage the household for day \d+\.",
                "",
                prompt,
                flags=re.IGNORECASE,
            ).strip().rstrip(" .")

            results = run_days(
                day,
                day,
                base_prompt,
            )

            day_result = results[0]

            return {
                "status": "ok",
                "error": None,
                "response": day_result["response"],
                "steps": day_result["steps"],
            }

        result = run_agent(prompt)

        return {
            "status": "ok",
            "error": None,
            "response": result["response"],
            "steps": result["steps"],
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