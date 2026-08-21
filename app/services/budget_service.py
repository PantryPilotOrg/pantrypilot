from app.services.profile_service import get_household_profile
from app.services.run_state_service import (
    INITIAL_SPENT_TO_DATE,
    get_run_state,
)


def get_budget_state() -> dict:
    """
    Return the household's current monthly budget state.
    """
    state = get_run_state()

    monthly_budget = get_household_profile()["monthly_budget"]
    spent_to_date = state["spent_to_date"]

    return {
        "monthly_budget": monthly_budget,
        "spent_to_date": spent_to_date,
        "remaining_budget": monthly_budget - spent_to_date,
    }


def add_spending(amount: float) -> dict:
    state = get_run_state()
    state["spent_to_date"] += amount

    return get_budget_state()


def reset_budget_state() -> None:
    state = get_run_state()
    state["spent_to_date"] = INITIAL_SPENT_TO_DATE