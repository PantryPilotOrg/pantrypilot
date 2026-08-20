from app.agent.runner import run_agent
from app.services.run_state_service import reset_run_state

MAX_RUN_DAYS = 7

def run_days(
    start_day: int,
    end_day: int,
    user_prompt: str = "Manage my kitchen",
) -> list[dict]:
    if start_day < 1:
        raise ValueError("Start day must be at least 1.")

    if end_day > MAX_RUN_DAYS:
        raise ValueError(
            f"PantryPilot currently supports up to {MAX_RUN_DAYS} days."
        )

    if start_day > end_day:
        raise ValueError("Start day cannot be after end day.")
    
    reset_run_state()

    results = []

    for day in range(start_day, end_day + 1):
        print(f"Starting simulation day {day}...")

        result = run_agent(
             f"{user_prompt} for day {day}."
        )

        print(f"Finished simulation day {day}.")

        results.append(
            {
                "simulation_day": day,
                "response": result["response"],
                "steps": result["steps"],
            }
        )

    return results