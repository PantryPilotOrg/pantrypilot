from contextvars import ContextVar


INITIAL_SPENT_TO_DATE = 720

_run_state: ContextVar[dict | None] = ContextVar(
    "pantrypilot_run_state",
    default=None,
)


def reset_run_state() -> None:
    _run_state.set(
        {
            "spent_to_date": INITIAL_SPENT_TO_DATE,
            "orders": [],
        }
    )


def get_run_state() -> dict:
    state = _run_state.get()

    if state is None:
        reset_run_state()
        state = _run_state.get()

    return state