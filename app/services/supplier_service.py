import csv

from app.config import DATA_DIR


def get_supplier_offers(item_ids: list[str]) -> list[dict]:
    """
    Load supplier offers from CSV for the requested item IDs.

    Args:
        item_ids: IDs of the requested products.

    Returns:
        A list of matching supplier offers.
    """
    suppliers_path = DATA_DIR / "suppliers.csv"
    requested_items = set(item_ids)
    offers = []

    with suppliers_path.open(
        mode="r",
        encoding="utf-8",
        newline="",
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


def initialize_supplier_basket(offer: dict) -> dict:
    """
    Create the initial basket structure for a supplier.
    """
    return {
        "supplier_id": offer["supplier_id"],
        "supplier_name": offer["supplier_name"],
        "supplier_type": offer["supplier_type"],
        "delivery_channel": offer["delivery_channel"],
        "delivery_fee": offer["delivery_fee"],
        "minimum_order": offer["minimum_order"],
        "earliest_available_day": offer["earliest_available_day"],
        "items": [],
        "subtotal": 0.0,
        "all_items_available": True,
    }


def evaluate_supplier_order(
    supplier_id: str,
    items: list[dict],
) -> dict | None:
    """
    Evaluate a requested basket for one supplier.

    The function checks product availability, calculates item and basket
    costs, validates the supplier's minimum-order requirement, and
    determines whether the basket can currently be ordered.

    Args:
        supplier_id: The supplier to evaluate.
        items: Requested item IDs and quantities.

    Returns:
        A structured basket evaluation for the supplier, or None if
        no matching supplier offers are found.
    """
    requested_ids = [item["item_id"] for item in items]
    offers = get_supplier_offers(requested_ids)

    supplier_offers = [
        offer
        for offer in offers
        if offer["supplier_id"] == supplier_id
    ]

    if not supplier_offers:
        return None

    basket = initialize_supplier_basket(supplier_offers[0])

    requested_items_by_id = {
        item["item_id"]: item
        for item in items
    }

    offered_item_ids = set()

    for offer in supplier_offers:
        item_id = offer["item_id"]
        offered_item_ids.add(item_id)

        requested_item = requested_items_by_id[item_id]
        quantity = requested_item["quantity"]
        item_total = offer["unit_price"] * quantity

        basket["items"].append(
            {
                "item_id": item_id,
                "quantity": quantity,
                "unit_price": offer["unit_price"],
                "available": offer["available"],
                "item_total": round(item_total, 2),
            }
        )

        if not offer["available"]:
            basket["all_items_available"] = False
        else:
            basket["subtotal"] += item_total

    requested_item_ids = set(requested_items_by_id)

    # A product may be missing completely from this supplier's CSV rows.
    missing_item_ids = requested_item_ids - offered_item_ids

    if missing_item_ids:
        basket["all_items_available"] = False

    basket["missing_item_ids"] = sorted(missing_item_ids)

    subtotal = round(basket["subtotal"], 2)
    minimum_order = basket["minimum_order"]

    minimum_order_met = subtotal >= minimum_order

    basket["subtotal"] = subtotal
    basket["minimum_order_met"] = minimum_order_met
    basket["amount_missing_for_minimum"] = round(
        max(0, minimum_order - subtotal),
        2,
    )
    basket["total_with_delivery"] = round(
        subtotal + basket["delivery_fee"],
        2,
    )
    basket["can_order"] = (
        basket["all_items_available"]
        and minimum_order_met
    )

    return basket


def compare_basket_costs(items: list[dict]) -> list[dict]:
    """
    Evaluate a proposed basket across all relevant suppliers.

    Args:
        items: Requested items, for example:
            [
                {"item_id": "milk", "quantity": 2},
                {"item_id": "rice", "quantity": 1},
            ]

    Returns:
        One complete basket evaluation per relevant supplier.
    """
    if not items:
        return []

    requested_ids = [item["item_id"] for item in items]
    offers = get_supplier_offers(requested_ids)

    supplier_ids = list(
        dict.fromkeys(
            offer["supplier_id"]
            for offer in offers
        )
    )

    results = []

    for supplier_id in supplier_ids:
        basket = evaluate_supplier_order(
            supplier_id=supplier_id,
            items=items,
        )

        if basket is not None:
            results.append(basket)

    return results