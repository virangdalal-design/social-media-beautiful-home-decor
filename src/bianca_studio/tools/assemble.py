"""Tool wrapper: assemble. FFmpeg delivery encode (Remotion composition is Phase 1 work).
Every paid call must log a row to generations (tools/db.py); this module makes none."""
import subprocess
from pathlib import Path

from .qc_technical import LOUDNESS_TARGET_LUFS, TRUE_PEAK_MAX_DBTP


def delivery_command(src: str | Path, dst: str | Path, spec: dict) -> list[str]:
    """FFmpeg args for the Instagram delivery file described in config/models.yaml."""
    w, h, fps = spec["width"], spec["height"], spec["fps"]
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,"
          f"crop={w}:{h},fps={fps},format={spec['pix_fmt']}")
    maxrate = spec["maxrate_mbps"]
    return [
        "ffmpeg", "-y", "-hide_banner", "-i", str(src),
        "-map", "0:v:0", "-map", "0:a:0?",
        "-vf", vf,
        "-c:v", spec["video_codec"], "-profile:v", spec["profile"], "-preset", "slow",
        "-crf", str(spec["crf"]), "-maxrate", f"{maxrate}M", "-bufsize", f"{maxrate * 2}M",
        "-g", str(fps * 2), "-flags", "+cgop", "-bf", "2",
        "-af", f"loudnorm=I={LOUDNESS_TARGET_LUFS}:TP={TRUE_PEAK_MAX_DBTP - 0.5}:LRA=11",
        "-c:a", spec["audio_codec"], "-b:a", f"{spec['audio_bitrate_kbps']}k",
        "-ar", str(spec["audio_sample_rate"]), "-ac", "2",
        "-movflags", "+faststart",
        str(dst),
    ]


def encode_delivery(src: str | Path, dst: str | Path, spec: dict) -> Path:
    subprocess.run(delivery_command(src, dst, spec), check=True, capture_output=True)
    return Path(dst)
