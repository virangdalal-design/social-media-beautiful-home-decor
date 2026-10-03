"""Tool wrapper: storage (Supabase Storage REST). Final renders go to the public bucket
because Instagram fetches the video by URL; everything else goes to the private bucket."""
import mimetypes
import os
from pathlib import Path

import httpx


def _base() -> tuple[str, dict]:
    url = os.environ["SUPABASE_URL"].rstrip("/")
    key = os.environ["SUPABASE_SERVICE_KEY"]
    return url, {"Authorization": f"Bearer {key}", "apikey": key}


def list_buckets(client: httpx.Client | None = None) -> list[dict]:
    url, headers = _base()
    resp = (client or httpx.Client(timeout=30)).get(f"{url}/storage/v1/bucket", headers=headers)
    resp.raise_for_status()
    return resp.json()


def upload(local: str | Path, dest: str, bucket: str | None = None, public: bool = False,
           client: httpx.Client | None = None) -> str:
    """Upload a file (upsert) and return its URL (public URL if the bucket is public)."""
    url, headers = _base()
    bucket = bucket or os.environ.get(
        "SUPABASE_STORAGE_BUCKET" if public else "SUPABASE_PRIVATE_BUCKET",
        "bianca-studio" if public else "bianca-studio-private")
    ctype = mimetypes.guess_type(str(local))[0] or "application/octet-stream"
    headers = {**headers, "Content-Type": ctype, "x-upsert": "true"}
    with open(local, "rb") as f:
        resp = (client or httpx.Client(timeout=300)).post(
            f"{url}/storage/v1/object/{bucket}/{dest}", headers=headers, content=f.read())
    resp.raise_for_status()
    if public:
        return f"{url}/storage/v1/object/public/{bucket}/{dest}"
    return f"{url}/storage/v1/object/{bucket}/{dest}"
