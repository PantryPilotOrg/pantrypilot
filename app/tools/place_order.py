from app.services.order_service import process_order


def place_order(
    simulation_day: int,
    supplier_id: str,
    items: list[dict],
) -> dict:
    """
    Validate and place an order with the selected supplier.

    Args:
        day: Current day number.
        supplier_id: The ID of the supplier selected by the agent.
        items: Requested item IDs and quantities.

    Returns:
        A compact structured result describing whether the
        order was successfully placed.
    """
    result = process_order(
        simulation_day=simulation_day,
        supplier_id=supplier_id,
        items=items,
    )

    if not result["success"]:
        return result

    return {
        "success": result["success"],
        "status": result["status"],
        "supplier_id": result["supplier_id"],
        "items": [
            {
                "item_id": item["item_id"],
                "quantity": item["quantity"],
            }
            for item in result["items"]
        ],
        "total_with_delivery": result["total_with_delivery"],
        "earliest_available_day": result[
            "earliest_available_day"
        ],
        "remaining_budget": result[
            "budget_after_order"
        ]["remaining_budget"],
    }