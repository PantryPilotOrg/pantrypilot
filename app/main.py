from pprint import pprint

from app.services.inventory_service import get_inventory_risks
from app.services.supplier_service import find_purchase_options


def main() -> None:
    print("\n--- Inventory risks for Day 2 ---")
    pprint(get_inventory_risks(2))

    print("\n--- Supplier options for milk and rice ---")
    pprint(find_purchase_options(["milk", "rice"]))


if __name__ == "__main__":
    main()