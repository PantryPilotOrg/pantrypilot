from app.services.run_state_service import get_run_state


def get_order_history() -> list[dict]:
    return get_run_state()["orders"]


def get_pending_orders(current_day: int) -> list[dict]:
    """
    Return earlier orders that are still relevant because their
    delivery window has not yet passed.
    """
    orders = get_order_history()

    return [
        order
        for order in orders
        if (
            order["simulation_day"] < current_day
            and current_day
            <= (
                order["simulation_day"]
                + order["earliest_available_day"]
            )
        )
    ]


def append_order(order: dict) -> None:
    get_order_history().append(order)


def reset_order_history() -> None:
    get_run_state()["orders"].clear()