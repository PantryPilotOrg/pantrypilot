from app.services.supplier_service import compare_basket_costs


def find_purchase_options(items: list[dict]) -> dict:
    """
    Return structured purchase options for the requested items.

    This high-level function will later be exposed to the Smart LLM
    as an agent tool.

    Args:
        items: Requested item IDs and quantities.

    Returns:
        A structured response containing the requested items
        and calculated purchase options for each supplier.
    """
    return {
        "requested_items": items,
        "options": compare_basket_costs(items),
    }