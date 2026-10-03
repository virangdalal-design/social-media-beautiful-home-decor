"""Node: qc. See agents/ and docs/02-ARCHITECTURE.md. TODO Phase 2."""
from ..state import JobState


def run(state: JobState) -> JobState:
    raise NotImplementedError("qc: implement in Phase 2")


def final(state: JobState) -> JobState:
    raise NotImplementedError


def final_router(state: JobState) -> str:
    return "pass" if (state.get("final_qc") or {}).get("pass") else "fail"
