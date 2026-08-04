from pprint import pprint

from app.tools.household_tool import get_household_state


def main() -> None:
    household_state = get_household_state(2)
    pprint(household_state)


if __name__ == "__main__":
    main()