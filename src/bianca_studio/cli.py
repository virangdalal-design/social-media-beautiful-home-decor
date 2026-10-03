"""Bianca Studio CLI.

  python -m bianca_studio.cli doctor [--offline]      check accounts, keys, tools
  python -m bianca_studio.cli check-video FILE        delivery spec check (free)
  python -m bianca_studio.cli encode SRC DST          FFmpeg delivery encode
  python -m bianca_studio.cli publish FILE --caption-file C [--yes]
  python -m bianca_studio.cli run --product ID        full pipeline (Phase 2)
"""
import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

import httpx

from .config import ROOT, delivery_spec, load_env, load_models

OK, WARN, FAIL = "\033[32mOK  \033[0m", "\033[33mWARN\033[0m", "\033[31mFAIL\033[0m"

REQUIRED_ENV = {
    "fal.ai": ["FAL_KEY"],
    "Gemini": ["GOOGLE_API_KEY"],
    "Anthropic": ["ANTHROPIC_API_KEY"],
    "Supabase": ["SUPABASE_URL", "SUPABASE_SERVICE_KEY", "SUPABASE_STORAGE_BUCKET"],
    "Instagram": ["META_ACCESS_TOKEN", "IG_USER_ID"],
}
OPTIONAL_ENV = {"ElevenLabs": ["ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID"]}


def _live_checks(http: httpx.Client) -> list[tuple[str, str, str]]:
    """One free read-only call per service. Returns (status, service, detail)."""
    out = []
    env = os.environ

    def attempt(name, fn):
        try:
            out.append((OK, name, fn()))
        except Exception as e:  # noqa: BLE001 — report every failure, keep checking the rest
            out.append((FAIL, name, str(e)[:200]))

    if env.get("ANTHROPIC_API_KEY"):
        def anthropic():
            r = http.get("https://api.anthropic.com/v1/models",
                         headers={"x-api-key": env["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"})
            r.raise_for_status()
            ids = {m["id"] for m in r.json()["data"]}
            missing = {v for v in load_models()["llm"].values()} - ids
            return f"{len(ids)} models" + (f"; config ids not listed: {sorted(missing)}" if missing else "")
        attempt("Anthropic", anthropic)

    if env.get("GOOGLE_API_KEY"):
        def gemini():
            r = http.get("https://generativelanguage.googleapis.com/v1beta/models",
                         params={"key": env["GOOGLE_API_KEY"], "pageSize": 1000})
            r.raise_for_status()
            names = {m["name"].removeprefix("models/") for m in r.json().get("models", [])}
            qc = load_models()["qc"]["vision_model"]
            return f"{len(names)} models; QC model '{qc}' " + ("found" if qc in names else "NOT found — fix qc.vision_model")
        attempt("Gemini", gemini)

    if env.get("SUPABASE_URL") and env.get("SUPABASE_SERVICE_KEY"):
        def supabase():
            from .tools.storage import list_buckets
            buckets = {b["name"]: b for b in list_buckets(http)}
            want = env.get("SUPABASE_STORAGE_BUCKET", "bianca-studio")
            if want not in buckets:
                raise RuntimeError(f"bucket '{want}' missing (have {sorted(buckets)})")
            if not buckets[want].get("public"):
                raise RuntimeError(f"bucket '{want}' must be public for Instagram to fetch videos")
            return f"bucket '{want}' public"
        attempt("Supabase", supabase)

    if env.get("META_ACCESS_TOKEN") and env.get("IG_USER_ID"):
        def instagram():
            from .tools.instagram import Instagram
            acct = Instagram(client=http).account()
            return f"@{acct.get('username')} ({acct.get('followers_count', '?')} followers)"
        attempt("Instagram", instagram)

    if env.get("ELEVENLABS_API_KEY"):
        def elevenlabs():
            r = http.get("https://api.elevenlabs.io/v1/user", headers={"xi-api-key": env["ELEVENLABS_API_KEY"]})
            r.raise_for_status()
            return f"tier {r.json().get('subscription', {}).get('tier', '?')}"
        attempt("ElevenLabs", elevenlabs)

    if env.get("FAL_KEY"):
        out.append((WARN, "fal.ai", "key present; not live-checked — first paid call proves it"))
    return out


def doctor(args) -> int:
    load_env()
    rows: list[tuple[str, str, str]] = []
    for service, keys in REQUIRED_ENV.items():
        missing = [k for k in keys if not os.environ.get(k)]
        rows.append((FAIL if missing else OK, service, f"missing {missing}" if missing else "env set"))
    for service, keys in OPTIONAL_ENV.items():
        missing = [k for k in keys if not os.environ.get(k)]
        rows.append((WARN if missing else OK, service, "optional, not set" if missing else "env set"))

    for tool in ("ffmpeg", "ffprobe"):
        rows.append((OK if shutil.which(tool) else FAIL, tool, shutil.which(tool) or "not installed"))
    rows.append((OK if shutil.which("npx") else WARN, "node/npx", "for Remotion" if shutil.which("npx") else "install Node 20+ for Remotion"))

    models = load_models()
    rows.append((OK if models.get("endpoints_verified") else WARN, "models.yaml",
                 "endpoint ids verified" if models.get("endpoints_verified")
                 else "endpoints_verified: false — confirm fal ids (docs/00-SETUP.md §B1)"))
    brand = [p for p in (ROOT / "assets" / "brand").glob("*") if p.name != ".gitkeep"]
    rows.append((OK if brand else WARN, "brand kit", f"{len(brand)} files" if brand else "assets/brand/ empty"))
    music = [p for p in (ROOT / "assets" / "music").glob("*") if p.name != ".gitkeep"]
    rows.append((OK if music else WARN, "music", f"{len(music)} tracks" if music else "assets/music/ empty (licensed tracks only)"))

    if not args.offline:
        with httpx.Client(timeout=30) as http:
            rows.extend(_live_checks(http))

    for status, name, detail in rows:
        print(f"{status} {name:<12} {detail}")
    failed = sum(1 for r in rows if r[0] == FAIL)
    print(f"\n{'All required checks passed.' if not failed else f'{failed} check(s) failed.'}")
    return 1 if failed else 0


def check_video(args) -> int:
    from .tools.qc_technical import check_delivery
    result = check_delivery(args.file, delivery_spec())
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


def encode(args) -> int:
    from .tools.assemble import encode_delivery
    out = encode_delivery(args.src, args.dst, delivery_spec())
    print(f"wrote {out}")
    return check_video(argparse.Namespace(file=out))


def publish(args) -> int:
    load_env()
    from .tools.instagram import Instagram
    from .tools.qc_technical import check_delivery
    from .tools.storage import upload

    result = check_delivery(args.file, delivery_spec())
    if not result["pass"]:
        print(json.dumps(result, indent=2))
        print("Refusing to publish: delivery checks failed.")
        return 1
    caption = Path(args.caption_file).read_text().strip()
    print(f"File: {args.file} ({result['facts']['duration_s']}s, {result['facts']['size_mb']} MB)")
    print(f"Caption:\n---\n{caption}\n---")
    if not args.yes:
        print("Dry run. Re-run with --yes after the human has approved this exact file and caption.")
        return 0
    dest = f"published/{time.strftime('%Y%m%d-%H%M%S')}-{Path(args.file).name}"
    video_url = upload(args.file, dest, public=True)
    print(f"Uploaded: {video_url}")
    media = Instagram().publish_reel(video_url, caption)
    print(f"Published: {media.get('permalink')} (id {media['id']})")
    return 0


def run(args) -> int:
    print("Full pipeline is Phase 2 (docs/01-PLAN.md). Phase 1 is run by hand.")
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bianca_studio", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("doctor", help="check accounts, keys and tools")
    p.add_argument("--offline", action="store_true", help="skip live API calls")
    p.set_defaults(fn=doctor)
    p = sub.add_parser("check-video", help="check a delivery file against the spec")
    p.add_argument("file")
    p.set_defaults(fn=check_video)
    p = sub.add_parser("encode", help="encode an edit/master to the Instagram delivery spec")
    p.add_argument("src")
    p.add_argument("dst")
    p.set_defaults(fn=encode)
    p = sub.add_parser("publish", help="publish an approved Reel to Instagram")
    p.add_argument("file")
    p.add_argument("--caption-file", required=True)
    p.add_argument("--yes", action="store_true", help="actually publish (otherwise dry run)")
    p.set_defaults(fn=publish)
    p = sub.add_parser("run", help="full pipeline (Phase 2)")
    p.add_argument("--product", required=True)
    p.set_defaults(fn=run)
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
