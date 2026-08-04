from app.services.inventory_service import (
    get_inventory_risks,
    get_inventory_with_estimates,
)
from app.services.profile_service import get_household_profile


def get_household_state(day: int) -> dict:
    """
    Return the current simulated household state.

    This high-level function will later be exposed to the Smart LLM
    as an agent tool.

    Args:
        day: Simulation day number, currently 1, 2, or 3.

    Returns:
        A structured response containing the household profile,
        enriched inventory, and concise inventory risks.
    """
    return {
        "simulation_day": day,
        "household_profile": get_household_profile(),
        "inventory": get_inventory_with_estimates(day),
        "risks": get_inventory_risks(day),
    }