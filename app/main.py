from pprint import pprint

from app.tools.household_tool import get_household_state
from app.tools.find_purchase_options import find_purchase_options
from app.tools.place_order import place_order

def main() -> None:
    household_state = get_household_state(2)
    pprint(household_state)

    purchase_options = find_purchase_options(
        [
            {"item_id": "milk", "quantity": 2},
            {"item_id": "rice", "quantity": 1},
        ]
    )

    print("\n--- Purchase Options ---")
    pprint(purchase_options)
    
    print("\n--- Place Order ---")

    order_result = place_order(
        supplier_id="ampm",
        items=[
            {"item_id": "milk", "quantity": 1},
        ]
    )

    pprint(order_result)

if __name__ == "__main__":
    main()