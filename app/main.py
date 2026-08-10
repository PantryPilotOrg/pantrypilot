from pprint import pprint

from app.tools.find_purchase_options import find_purchase_options
from app.tools.place_order import place_order


def main() -> None:
    requested_items = [
        {"item_id": "milk", "quantity": 2},
        {"item_id": "yogurt", "quantity": 5},
        {"item_id": "eggs", "quantity": 1},
        {"item_id": "bread", "quantity": 2},
        {"item_id": "rice", "quantity": 2},
        {"item_id": "pasta", "quantity": 3},
        {"item_id": "tomatoes", "quantity": 1.3},
        {"item_id": "cucumbers", "quantity": 1.4},
        {"item_id": "chicken", "quantity": 2},
        {"item_id": "coffee", "quantity": 1},
        {"item_id": "cat_food", "quantity": 1},
    ]

    print("\n--- Purchase Options ---")
    pprint(
        find_purchase_options(requested_items),
        sort_dicts=False,
    )

    print("\n--- Place Order ---")
    order_result = place_order(
        supplier_id="ampm",
        items=[
            {"item_id": "milk", "quantity": 1},
        ],
    )

    pprint(order_result, sort_dicts=False)


if __name__ == "__main__":
    main()