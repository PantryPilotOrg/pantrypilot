from app.services.budget_service import reset_budget_state
from app.services.order_history_service import reset_order_history


def reset_simulation_state() -> None:
    reset_order_history()
    reset_budget_state()