"""Tool wrapper: qc_technical. ffprobe/ffmpeg checks of a delivery file against
docs/03-QUALITY-BAR.md and Instagram's Reels upload limits. Free (no paid calls)."""
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path

# Instagram hard limits (Content Publishing API, Reels tab eligibility).
IG_MIN_FPS, IG_MAX_FPS = 23, 60
IG_MIN_DURATION_S, IG_MAX_DURATION_S = 5, 90
IG_MAX_SIZE_MB = 100
IG_MAX_AUDIO_HZ = 48000

LOUDNESS_TARGET_LUFS = -14.0
LOUDNESS_TOLERANCE_LU = 1.5
TRUE_PEAK_MAX_DBTP = -1.0


def probe(path: str | Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


def moov_before_mdat(path: str | Path) -> bool:
    """True if the MP4 'moov' atom precedes 'mdat' (i.e. encoded with +faststart)."""
    with open(path, "rb") as f:
        while True:
            header = f.read(8)
            if len(header) < 8:
                return False
            size = int.from_bytes(header[:4], "big")
            kind = header[4:8]
            if kind == b"moov":
                return True
            if kind == b"mdat":
                return False
            if size == 1:
                size = int.from_bytes(f.read(8), "big")
                f.seek(size - 16, 1)
            elif size == 0:
                return False
            else:
                f.seek(size - 8, 1)


def loudness(path: str | Path) -> dict | None:
    """Integrated loudness (LUFS) and true peak (dBTP) via ffmpeg loudnorm analysis."""
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-af", "loudnorm=print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=False,
    )
    match = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", out.stderr)
    if not match:
        return None
    data = json.loads(match.group(0))
    return {"integrated_lufs": float(data["input_i"]), "true_peak_dbtp": float(data["input_tp"])}


def check_delivery(path: str | Path, spec: dict) -> dict:
    """Return {"pass": bool, "fails": [...], "warnings": [...], "facts": {...}}."""
    path = Path(path)
    info = probe(path)
    fails: list[str] = []
    warnings: list[str] = []

    video = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    fmt = info["format"]
    size_mb = int(fmt["size"]) / 1_000_000
    duration = float(fmt.get("duration", 0))
    facts: dict = {"size_mb": round(size_mb, 2), "duration_s": round(duration, 2), "container": fmt["format_name"]}

    if path.suffix.lower() not in (".mp4", ".mov"):
        fails.append(f"container {path.suffix} not MP4/MOV")
    if size_mb > min(spec.get("max_size_mb", IG_MAX_SIZE_MB), IG_MAX_SIZE_MB):
        fails.append(f"file {size_mb:.1f} MB over limit {spec.get('max_size_mb', IG_MAX_SIZE_MB)} MB")
    if not IG_MIN_DURATION_S <= duration <= IG_MAX_DURATION_S:
        fails.append(f"duration {duration:.1f}s outside {IG_MIN_DURATION_S}-{IG_MAX_DURATION_S}s Reels range")

    if video is None:
        fails.append("no video stream")
    else:
        w, h = int(video["width"]), int(video["height"])
        fps = float(Fraction(video.get("avg_frame_rate", "0/1"))) if video.get("avg_frame_rate", "0/0") != "0/0" else 0.0
        facts.update(width=w, height=h, fps=round(fps, 3), video_codec=video["codec_name"],
                     profile=video.get("profile"), pix_fmt=video.get("pix_fmt"),
                     bitrate_mbps=round(int(video.get("bit_rate", 0)) / 1e6, 2))
        if (w, h) != (spec["width"], spec["height"]):
            fails.append(f"resolution {w}x{h}, expected {spec['width']}x{spec['height']}")
        if abs(w / h - 9 / 16) > 0.01:
            fails.append(f"aspect {w}:{h} is not 9:16")
        if video["codec_name"] not in ("h264", "hevc"):
            fails.append(f"video codec {video['codec_name']} not H.264/HEVC")
        if video.get("pix_fmt") != spec.get("pix_fmt", "yuv420p"):
            fails.append(f"pix_fmt {video.get('pix_fmt')} not {spec.get('pix_fmt', 'yuv420p')}")
        if not IG_MIN_FPS <= fps <= IG_MAX_FPS:
            fails.append(f"fps {fps:.2f} outside {IG_MIN_FPS}-{IG_MAX_FPS}")
        elif abs(fps - spec["fps"]) > 0.01:
            fails.append(f"fps {fps:.2f}, expected {spec['fps']}")
        if video.get("field_order", "progressive") not in ("progressive", "unknown"):
            fails.append(f"interlaced video ({video['field_order']})")

    if audio is None:
        warnings.append("no audio stream (Instagram accepts it; add music or ambience)")
    else:
        sr = int(audio.get("sample_rate", 0))
        facts.update(audio_codec=audio["codec_name"], audio_hz=sr, audio_channels=audio.get("channels"))
        if audio["codec_name"] != "aac":
            fails.append(f"audio codec {audio['codec_name']} not AAC")
        if sr > IG_MAX_AUDIO_HZ:
            fails.append(f"audio sample rate {sr} > {IG_MAX_AUDIO_HZ}")
        if audio.get("channels", 0) > 2:
            fails.append(f"{audio['channels']} audio channels; Instagram needs mono or stereo")
        loud = loudness(path)
        if loud:
            facts.update(loud)
            if abs(loud["integrated_lufs"] - LOUDNESS_TARGET_LUFS) > LOUDNESS_TOLERANCE_LU:
                warnings.append(f"loudness {loud['integrated_lufs']} LUFS, target {LOUDNESS_TARGET_LUFS}")
            if loud["true_peak_dbtp"] > TRUE_PEAK_MAX_DBTP:
                fails.append(f"true peak {loud['true_peak_dbtp']} dBTP > {TRUE_PEAK_MAX_DBTP} (clipping risk)")

    if path.suffix.lower() == ".mp4" and not moov_before_mdat(path):
        fails.append("moov atom not at front (encode with -movflags +faststart)")

    return {"pass": not fails, "fails": fails, "warnings": warnings, "facts": facts}
