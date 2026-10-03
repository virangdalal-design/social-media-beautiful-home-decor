import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / "config" / ".env"


def load_env(path: Path = ENV_FILE) -> None:
    """Load KEY=VALUE lines from config/.env into os.environ (existing env wins)."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_models() -> dict:
    return yaml.safe_load((ROOT / "config" / "models.yaml").read_text())


def pick_video_models(purpose: str, n: int | None = None, draft: bool = False) -> list[dict]:
    """Ordered candidates for a shot purpose; `n` defaults to video.defaults.best_of."""
    video = load_models()["video"]
    tiers = video["tiers"]
    tier = "draft" if draft else purpose
    if tier not in tiers:
        raise KeyError(f"no video tier '{tier}' in config/models.yaml")
    n = n or video["defaults"]["best_of"]
    return tiers[tier][:n]


def pick_video_model(purpose: str, draft: bool = False) -> dict:
    return pick_video_models(purpose, n=1, draft=draft)[0]


def delivery_spec() -> dict:
    return load_models()["finishing"]["delivery"]
