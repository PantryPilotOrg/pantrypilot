from app.services.order_service import process_order


def place_order(
    supplier_id: str,
    items: list[dict],
) -> dict:
    """
    Validate and simulate placing an order with the selected supplier.

    This high-level function will later be exposed to the Smart LLM
    as an agent tool.

    The tool is independent from find_purchase_options. It receives
    only the selected supplier and requested items, while the service
    validates the order using the current supplier data.

    Args:
        supplier_id: The ID of the supplier selected by the agent.
        items: Requested item IDs and quantities.

    Returns:
        A structured result describing whether the simulated order
        was successfully placed.

    Note:
        This MVP version does not update the household budget,
        inventory, order history, or long-term memory.
    """
    return process_order(
        supplier_id=supplier_id,
        items=items,
    )