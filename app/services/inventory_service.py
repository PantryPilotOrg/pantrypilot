import csv

from app.config import DATA_DIR

def get_inventory(day: int) -> list[dict]:
    """
    Load mocked household inventory for a selected simulation day.

    Args:
        day: Simulation day number, currently 1, 2, or 3.

    Returns:
        A list of inventory item dictionaries.

    Raises:
        ValueError: If the requested day is invalid.
        FileNotFoundError: If the CSV file does not exist.
    """
    if day not in {1, 2, 3}:
        raise ValueError("Day must be 1, 2, or 3.")

    inventory_path = DATA_DIR / f"inventory_day_{day}.csv"
    items = []

    with inventory_path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            items.append(
                {
                    "item_id": row["item_id"],
                    "item_name": row["item_name"],
                    "quantity": float(row["quantity"]),
                    "unit": row["unit"],
                    "days_until_expiry": (
                        int(row["days_until_expiry"])
                        if row["days_until_expiry"]
                        else None
                    ),
                }
            )

    return items

def get_consumption_patterns() -> dict[str, dict]:
    """
    Load mocked household consumption patterns.

    Returns:
        A dictionary keyed by item_id.
    """
    patterns_path = DATA_DIR / "consumption_patterns.csv"
    patterns = {}

    with patterns_path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            patterns[row["item_id"]] = {
                "estimated_units_per_day": float(
                    row["estimated_units_per_day"]
                ),
                "confidence": row["confidence"],
                "source": row["source"],
            }

    return patterns


def get_stock_targets() -> dict[str, dict]:
    """
    Load the household's normal stock preferences.

    target_quantity is the preferred quantity after PantryPilot has already
    decided that replenishment is appropriate. Being below the target does
    not automatically mean that an item should be purchased.
    """
    targets_path = DATA_DIR / "stock_targets.csv"
    targets = {}

    with targets_path.open(mode="r", encoding="utf-8", newline="", ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            targets[row["item_id"]] = {
                "is_regular_item": (
                    row["is_regular_item"].lower() == "true"
                ),
                "target_quantity": float(row["target_quantity"]),
                "priority": row["priority"],
            }

    return targets

def get_inventory_with_estimates(day: int) -> list[dict]:
    """
    Combine current inventory with learned consumption patterns and
    household stock preferences.
    """
    inventory = get_inventory(day)
    consumption_patterns = get_consumption_patterns()
    stock_targets = get_stock_targets()

    enriched_inventory = []

    for item in inventory:
        item_id = item["item_id"]
        pattern = consumption_patterns.get(item_id)
        target = stock_targets.get(item_id)

        enriched_item = item.copy()

        if pattern is None:
            enriched_item["consumption_pattern"] = None
            estimated_days = None
        else:
            daily_consumption = pattern["estimated_units_per_day"]
            quantity = item["quantity"]

            estimated_days = (
                quantity / daily_consumption
                if daily_consumption > 0
                else None
            )

            enriched_item["consumption_pattern"] = pattern

        enriched_item["estimated_days_until_depletion"] = (
            round(estimated_days, 2)
            if estimated_days is not None
            else None
        )

        if target is None:
            enriched_item["stock_target"] = None
            enriched_item["quantity_to_target"] = None
        else:
            target_quantity = target["target_quantity"]

            quantity_to_target = max(
                0,
                target_quantity - item["quantity"],
            )

            enriched_item["stock_target"] = target
            enriched_item["quantity_to_target"] = round(
                quantity_to_target,
                2,
            )

        enriched_inventory.append(enriched_item)

    return enriched_inventory

def get_inventory_risks(day: int) -> list[dict]:
    """
    Identify depletion and expiry risks for a selected simulation day.
    """
    inventory = get_inventory_with_estimates(day)
    risks = []

    for item in inventory:
        depletion_days = item["estimated_days_until_depletion"]
        expiry_days = item["days_until_expiry"]

        if depletion_days is not None and depletion_days <= 1:
            risks.append(
                {
                    "item_id": item["item_id"],
                    "risk_type": "depletion",
                    "details": (
                        f"Estimated to run out in "
                        f"{depletion_days} day(s)."
                    ),
                }
            )

        if (
            expiry_days is not None
            and expiry_days <= 1
            and item["quantity"] > 0
        ):
            risks.append(
                {
                    "item_id": item["item_id"],
                    "risk_type": "expiry",
                    "details": (
                        f"{item['quantity']} {item['unit']}(s) "
                        f"expire in {expiry_days} day(s)."
                    ),
                }
            )

    return risks
