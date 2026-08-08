import csv

from app.config import DATA_DIR


def get_upcoming_events(day: int) -> list[dict]:
    """
    Load events occurring on or after the selected simulation day.

    Args:
        day: Current simulation day.

    Returns:
        Upcoming events ordered by simulation day.
    """
    events_path = DATA_DIR / "events.csv"
    events = []

    with events_path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            event_day = int(row["simulation_day"])

            if event_day < day:
                continue

            events.append(
                {
                    "event_id": row["event_id"],
                    "event_type": row["event_type"],
                    "simulation_day": event_day,
                    "days_until_event": event_day - day,
                    "guest_count": (
                        int(row["guest_count"])
                        if row["guest_count"]
                        else None
                    ),
                    "notes": row["notes"],
                }
            )

    return sorted(
        events,
        key=lambda event: event["simulation_day"],
    )