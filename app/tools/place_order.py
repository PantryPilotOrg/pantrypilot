from app.services.order_service import process_order


def place_order(
    simulation_day: int,
    supplier_id: str,
    items: list[dict],
) -> dict:
    """
    Validate and simulate placing an order with the selected supplier.

    Args:
        simulation_day: Current simulation day.
        supplier_id: The ID of the supplier selected by the agent.
        items: Requested item IDs and quantities.

    Returns:
        A structured result describing whether the simulated order
        was successfully placed.
    """
    return process_order(
        simulation_day=simulation_day,
        supplier_id=supplier_id,
        items=items,
    )