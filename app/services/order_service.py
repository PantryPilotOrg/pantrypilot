from app.services.supplier_service import evaluate_supplier_order
from app.services.budget_service import add_spending, get_budget_state
from app.services.order_history_service import append_order

def process_order(
    simulation_day: int,
    supplier_id: str,
    items: list[dict],
) -> dict:
    """
    Validate and simulate an order with the selected supplier.

    The service evaluates only the supplier selected by the agent.
    It does not depend on the output structure of find_purchase_options.

    Args:
        supplier_id: The ID of the supplier selected for the order.
        items: Requested item IDs and quantities.
        simulation_day: Current simulation day.

    Returns:
        A structured mock order confirmation when the order is valid,
        or a structured rejection explaining why it cannot be placed.

    Note:
        This MVP version does not update budget, inventory,
        order history, or long-term memory.
    """
    if not items:
        return {
            "success": False,
            "status": "rejected",
            "error_code": "EMPTY_ORDER",
            "message": "The order does not contain any items.",
        }

    for item in items:
        if item.get("quantity", 0) <= 0:
            return {
                "success": False,
                "status": "rejected",
                "error_code": "INVALID_QUANTITY",
                "message": (
                    "All requested item quantities must be greater than zero."
                ),
            }

    selected_option = evaluate_supplier_order(
        supplier_id=supplier_id,
        items=items,
    )

    if selected_option is None:
        return {
            "success": False,
            "status": "rejected",
            "error_code": "SUPPLIER_NOT_FOUND",
            "supplier_id": supplier_id,
            "message": (
                f"No matching offers were found for supplier "
                f"'{supplier_id}'."
            ),
        }

    if not selected_option["all_items_available"]:
        return {
            "success": False,
            "status": "rejected",
            "error_code": "ITEMS_UNAVAILABLE",
            "supplier_id": supplier_id,
            "missing_item_ids": selected_option["missing_item_ids"],
            "message": (
                "Not all requested items are available "
                "from this supplier."
            ),
        }

    if not selected_option["minimum_order_met"]:
        return {
            "success": False,
            "status": "rejected",
            "error_code": "MINIMUM_ORDER_NOT_MET",
            "supplier_id": supplier_id,
            "amount_missing_for_minimum": selected_option[
                "amount_missing_for_minimum"
            ],
            "message": (
                "The supplier's minimum order requirement is not met."
            ),
        }

    budget = get_budget_state()
    order_total = selected_option["total_with_delivery"]

    if order_total > budget["remaining_budget"]:
        return {
            "success": False,
            "status": "rejected",
            "error_code": "BUDGET_EXCEEDED",
            "supplier_id": supplier_id,
            "order_total": order_total,
            "remaining_budget": budget["remaining_budget"],
            "message": (
                "The order total exceeds the household's remaining budget."
            ),
        }

    updated_budget = add_spending(order_total)
    order_record = {
        "simulation_day": simulation_day,
        "supplier_id": selected_option["supplier_id"],
        "supplier_name": selected_option["supplier_name"],
        "items": selected_option["items"],
        "subtotal": selected_option["subtotal"],
        "delivery_fee": selected_option["delivery_fee"],
        "total_with_delivery": selected_option["total_with_delivery"],
        "earliest_available_day": selected_option["earliest_available_day"],
        "budget_after_order": updated_budget,
    }

    append_order(order_record)

    return {
        "success": True,
        "status": "confirmed",
        "supplier_id": selected_option["supplier_id"],
        "supplier_name": selected_option["supplier_name"],
        "items": selected_option["items"],
        "subtotal": selected_option["subtotal"],
        "delivery_fee": selected_option["delivery_fee"],
        "total_with_delivery": selected_option[
            "total_with_delivery"
        ],
        "earliest_available_day": selected_option[
            "earliest_available_day"
        ],
        "budget_after_order": updated_budget,
        "message": "Mock order placed successfully.",
    }