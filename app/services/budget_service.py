import json

from app.config import DATA_DIR
from app.services.profile_service import get_household_profile

INITIAL_SPENT_TO_DATE = 720

def get_budget_state() -> dict:
    """
    Return the household's current monthly budget state.
    """
    budget_path = DATA_DIR / "budget_state.json"

    with budget_path.open(mode="r", encoding="utf-8") as file:
        budget_data = json.load(file)

    monthly_budget = get_household_profile()["monthly_budget"]
    spent_to_date = budget_data["spent_to_date"]

    return {
        "monthly_budget": monthly_budget,
        "spent_to_date": spent_to_date,
        "remaining_budget": monthly_budget - spent_to_date,
    }

def reset_budget_state() -> None:
    with open(DATA_DIR / "budget_state.json", "w", encoding="utf-8") as file:
        json.dump(
            {"spent_to_date": INITIAL_SPENT_TO_DATE},
            file,
            indent=2
        )