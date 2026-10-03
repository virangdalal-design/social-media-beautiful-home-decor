"""Node: producer. See agents/ and docs/02-ARCHITECTURE.md. TODO Phase 2."""
from ..state import JobState


def run(state: JobState) -> JobState:
    raise NotImplementedError("producer: implement in Phase 2")


def run_all_shots(state: JobState) -> JobState:
    """For each shot: keyframe -> keyframe_qc -> video -> shot_qc, with retry caps from config."""
    raise NotImplementedError
