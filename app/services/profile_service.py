import json

from app.config import DATA_DIR


def get_household_profile() -> dict:
    """
    Load the simulated household's stable initial setup data.
    """
    profile_path = DATA_DIR / "household_profile.json"

    with profile_path.open(mode="r", encoding="utf-8") as file:
        return json.load(file)