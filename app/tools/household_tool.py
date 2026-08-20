from app.services.inventory_service import (
    get_inventory_risks,
    get_inventory_with_estimates,
)
from app.services.profile_service import get_household_profile
from app.services.event_service import get_upcoming_events
from app.services.budget_service import get_budget_state
from app.services.order_history_service import get_pending_orders

def _compact_inventory(inventory: list[dict]) -> list[dict]:
    compact = []

    for item in inventory:
        stock_target = item["stock_target"]

        compact.append(
            {
                "item_id": item["item_id"],
                "quantity": item["quantity"],
                "unit": item["unit"],
                "days_until_expiry": item["days_until_expiry"],
                "estimated_days_until_depletion": item[
                    "estimated_days_until_depletion"
                ],
                "target_quantity": (
                    stock_target["target_quantity"]
                    if stock_target
                    else None
                ),
                "priority": (
                    stock_target["priority"]
                    if stock_target
                    else None
                ),
                "quantity_to_target": item["quantity_to_target"],
            }
        )

    return compact

def _compact_pending_orders(orders: list[dict]) -> list[dict]:
    compact = []

    for order in orders:
        compact.append(
            {
                "order_day": order["simulation_day"],
                "supplier_id": order["supplier_id"],
                "items": [
                    {
                        "item_id": item["item_id"],
                        "quantity": item["quantity"],
                    }
                    for item in order["items"]
                ],
                "earliest_available_day": order[
                    "earliest_available_day"
                ],
            }
        )

    return compact

def get_household_state(day: int) -> dict:
    """
    Return the current household state for the requested day.

    This high-level function will later be exposed to the Smart LLM
    as an agent tool.

    Args:
        day: Household data day, currently 1 through 7.

    Returns:
        A structured response containing the household profile,
        enriched inventory, and concise inventory risks.
    """
    inventory = get_inventory_with_estimates(day)
    profile = get_household_profile()
    budget = get_budget_state()

    return {
        "day": day,
        "household_profile": {
            "household_size": profile["household_size"],
            "substitutions_allowed": profile["substitutions_allowed"],
            "pets": profile["pets"],
            "notes": profile["notes"],
        },
        "budget": {
            "monthly_budget": budget["monthly_budget"],
            "remaining_budget": budget["remaining_budget"],
        },
        "inventory": _compact_inventory(inventory),
        "risks": [
            {
                "item_id": risk["item_id"],
                "risk_type": risk["risk_type"],
            }
            for risk in get_inventory_risks(day)
        ],
        "upcoming_events": [
            {
                "event_type": event["event_type"],
                "event_day": event["simulation_day"],
                "days_until_event": event["days_until_event"],
                "guest_count": event["guest_count"],
                "notes": event["notes"],
            }
            for event in get_upcoming_events(day)
        ],
        "pending_orders": _compact_pending_orders(
            get_pending_orders(day)
        ),
    }