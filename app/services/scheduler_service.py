import time

from app.agent.runner import run_agent
from app.services.run_state_service import reset_run_state


MAX_RUN_DAYS = 7
MAX_DAYS_PER_RUN = 3


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

    if end_day - start_day + 1 > MAX_DAYS_PER_RUN:
        raise ValueError(
            f"A simulation run can include up to "
            f"{MAX_DAYS_PER_RUN} consecutive days."
        )

    reset_run_state()

    results = []
    run_start = time.perf_counter()

    for day in range(start_day, end_day + 1):
        day_start = time.perf_counter()

        print(f"Starting simulation day {day}...")

        result = run_agent(
            f"{user_prompt} for day {day}."
        )

        day_elapsed = time.perf_counter() - day_start

        print(
            f"Finished simulation day {day} "
            f"in {day_elapsed:.2f} seconds."
        )

        results.append(
            {
                "simulation_day": day,
                "response": result["response"],
                "steps": result["steps"],
            }
        )

    total_elapsed = time.perf_counter() - run_start

    print(
        f"Simulation days {start_day}-{end_day} "
        f"finished in {total_elapsed:.2f} seconds."
    )

    return results