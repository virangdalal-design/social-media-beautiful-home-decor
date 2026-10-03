import shutil
import subprocess

import pytest

from bianca_studio.config import delivery_spec
from bianca_studio.tools.assemble import encode_delivery
from bianca_studio.tools.qc_technical import check_delivery

pytestmark = pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg not installed")


def _source(path, w=1280, h=720, seconds=6):
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "lavfi", "-i", f"testsrc2=size={w}x{h}:rate=25:duration={seconds}",
         "-f", "lavfi", "-i", f"sine=frequency=440:sample_rate=44100:duration={seconds}",
         "-c:v", "libx264", "-pix_fmt", "yuv444p", "-c:a", "aac", str(path)],
        check=True,
    )
    return path


def test_raw_source_fails_spec(tmp_path):
    result = check_delivery(_source(tmp_path / "raw.mp4"), delivery_spec())
    assert not result["pass"]
    joined = " ".join(result["fails"])
    assert "resolution" in joined and "pix_fmt" in joined and "fps" in joined


def test_delivery_encode_passes_spec(tmp_path):
    out = encode_delivery(_source(tmp_path / "raw.mp4"), tmp_path / "reel.mp4", delivery_spec())
    result = check_delivery(out, delivery_spec())
    assert result["pass"], result
    f = result["facts"]
    assert (f["width"], f["height"], f["fps"]) == (1080, 1920, 30)
    assert f["audio_hz"] == 48000


def test_too_short_fails(tmp_path):
    out = encode_delivery(_source(tmp_path / "raw.mp4", seconds=3), tmp_path / "short.mp4", delivery_spec())
    assert any("duration" in x for x in check_delivery(out, delivery_spec())["fails"])
