import csv

from app.config import DATA_DIR

def find_purchase_options(items: list[str]) -> list[dict]:
    """
    Load supplier offers from CSV for the requested item IDs.
    """
    suppliers_path = DATA_DIR / "suppliers.csv"
    requested_items = set(items)
    offers = []

    with suppliers_path.open(
        mode="r",
        encoding="utf-8",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["item_id"] not in requested_items:
                continue

            offers.append(
                {
                    "supplier_id": row["supplier_id"],
                    "supplier_name": row["supplier_name"],
                    "supplier_type": row["supplier_type"],
                    "item_id": row["item_id"],
                    "unit_price": float(row["unit_price"]),
                    "available": row["available"].lower() == "true",
                    "delivery_channel": row["delivery_channel"],
                    "delivery_fee": float(row["delivery_fee"]),
                    "minimum_order": float(row["minimum_order"]),
                    "earliest_available_day": int(
                        row["earliest_available_day"]
                    ),
                }
            )

    return offers

def compare_basket_costs(items: list[dict]) -> list[dict]:
    """
    Calculate the cost of a proposed basket at each supplier.

    Args:
        items: Requested items, for example:
            [
                {"item_id": "milk", "quantity": 2},
                {"item_id": "rice", "quantity": 1}
            ]

    Returns:
        One basket-cost result per supplier.
    """
    requested_ids = [item["item_id"] for item in items]
    offers = find_purchase_options(requested_ids)

    suppliers = {}

    for offer in offers:
        supplier_id = offer["supplier_id"]

        if supplier_id not in suppliers:
            suppliers[supplier_id] = {
                "supplier_id": supplier_id,
                "supplier_name": offer["supplier_name"],
                "supplier_type": offer["supplier_type"],
                "delivery_channel": offer["delivery_channel"],
                "delivery_fee": offer["delivery_fee"],
                "minimum_order": offer["minimum_order"],
                "earliest_available_day": offer[
                    "earliest_available_day"
                ],
                "items": [],
                "subtotal": 0.0,
                "all_items_available": True,
            }

        requested_item = next(
            item
            for item in items
            if item["item_id"] == offer["item_id"]
        )

        quantity = requested_item["quantity"]
        item_total = offer["unit_price"] * quantity

        suppliers[supplier_id]["items"].append(
            {
                "item_id": offer["item_id"],
                "quantity": quantity,
                "unit_price": offer["unit_price"],
                "available": offer["available"],
                "item_total": round(item_total, 2),
            }
        )

        if not offer["available"]:
            suppliers[supplier_id]["all_items_available"] = False
        else:
            suppliers[supplier_id]["subtotal"] += item_total

    results = []

    for supplier in suppliers.values():
        subtotal = round(supplier["subtotal"], 2)
        minimum_order = supplier["minimum_order"]

        minimum_order_met = subtotal >= minimum_order
        total = subtotal + supplier["delivery_fee"]

        supplier["subtotal"] = subtotal
        supplier["minimum_order_met"] = minimum_order_met
        supplier["amount_missing_for_minimum"] = round(
            max(0, minimum_order - subtotal),
            2,
        )
        supplier["total_with_delivery"] = round(total, 2)

        results.append(supplier)

    return results