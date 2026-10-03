from typing import Any, TypedDict


class ShotState(TypedDict, total=False):
    spec: dict[str, Any]
    keyframe_url: str | None
    keyframe_attempts: int
    video_url: str | None
    video_attempts: int
    model: str | None
    qc_reports: list[dict[str, Any]]
    cost_usd: float
    status: str  # pending|keyframe_ok|video_ok|needs_human|done


class JobState(TypedDict, total=False):
    job_id: str
    product_brief: dict[str, Any]
    angles: list[dict[str, Any]]
    selected_angle_ids: list[str]
    shot_lists: dict[str, dict[str, Any]]
    shots: dict[str, ShotState]
    voice_url: str | None
    assembled_url: str | None
    final_qc: dict[str, Any] | None
    approval: dict[str, Any] | None
    total_cost_usd: float
    errors: list[str]
