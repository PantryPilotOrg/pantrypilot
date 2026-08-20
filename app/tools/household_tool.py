from app.services.inventory_service import (
    get_inventory_risks,
    get_inventory_with_estimates,
)
from app.services.profile_service import get_household_profile
from app.services.event_service import get_upcoming_events
from app.services.budget_service import get_budget_state
from app.services.order_history_service import get_order_history


def get_household_state(day: int) -> dict:
    """
    Return the current simulated household state.

    This high-level function will later be exposed to the Smart LLM
    as an agent tool.

    Args:
        day: Simulation day number within the selected simulation range,
     currently 1 through 7.

    Returns:
        A structured response containing the household profile,
        enriched inventory, and concise inventory risks.
    """
    return {
        "simulation_day": day,
        "household_profile": get_household_profile(),
        "budget": get_budget_state(),
        "inventory": get_inventory_with_estimates(day),
        "risks": get_inventory_risks(day),
        "upcoming_events": get_upcoming_events(day),
        "recent_orders": get_order_history(),
    }