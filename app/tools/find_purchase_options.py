from app.services.supplier_service import compare_basket_costs


def find_purchase_options(items: list[dict]) -> dict:
    """
        Return compact supplier purchase options for the requested household items.

        Args:
            items: Requested item IDs and quantities.

        Returns:
            A compact structured response containing the requested items
            and the relevant purchase options for each supplier.
    """
    options = compare_basket_costs(items)

    compact_supplier_options = []

    for option in options:
        compact_supplier_options.append(
            {
                "supplier_id": option["supplier_id"],
                "supplier_type": option["supplier_type"],
                "delivery_fee": option["delivery_fee"],
                "minimum_order": option["minimum_order"],
                "earliest_available_day": option[
                    "earliest_available_day"
                ],
                "items": [
                    {
                        "item_id": item["item_id"],
                        "quantity": item["quantity"],
                        "unit_price": item["unit_price"],
                        "available": item["available"],
                    }
                    for item in option["items"]
                ],
                "subtotal": option["subtotal"],
                "missing_item_ids": option["missing_item_ids"],
                "minimum_order_met": option["minimum_order_met"],
                "amount_missing_for_minimum": option[
                    "amount_missing_for_minimum"
                ],
                "total_with_delivery": option[
                    "total_with_delivery"
                ],
                "can_order": option["can_order"],
            }
        )

    return {
        "requested_items": items,
        "options": compact_supplier_options,
    }