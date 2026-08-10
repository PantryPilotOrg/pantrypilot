from app.services.supplier_service import evaluate_supplier_order


def process_order(
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
        "message": "Mock order placed successfully.",
    }