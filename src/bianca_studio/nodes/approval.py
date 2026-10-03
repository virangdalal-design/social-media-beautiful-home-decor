"""Node: approval. See agents/ and docs/02-ARCHITECTURE.md. TODO Phase 2."""
from ..state import JobState


def run(state: JobState) -> JobState:
    raise NotImplementedError("approval: implement in Phase 2")


def pick_angles(state: JobState) -> JobState:
    return state  # human sets selected_angle_ids via API before resume


def decide(state: JobState) -> JobState:
    return state  # human sets approval via API before resume


def route(state: JobState) -> JobState:
    return state


def router(state: JobState) -> str:
    a = state.get("approval") or {}
    if a.get("status") == "approved":
        return "approved"
    return a.get("routed_to", "producer")
