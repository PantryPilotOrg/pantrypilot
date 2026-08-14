import json

from app.config import DATA_DIR


ORDER_HISTORY_FILE = DATA_DIR / "order_history.json"


def get_order_history() -> list[dict]:
    with open(ORDER_HISTORY_FILE, encoding="utf-8") as file:
        return json.load(file)


def append_order(order: dict) -> None:
    orders = get_order_history()
    orders.append(order)

    with open(ORDER_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=2)

def reset_order_history() -> None:
    with open(ORDER_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump([], file, indent=2)