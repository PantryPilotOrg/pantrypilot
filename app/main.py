from pprint import pprint

from app.tools.household_tool import get_household_state
from app.tools.find_purchase_options import find_purchase_options

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

if __name__ == "__main__":
    main()