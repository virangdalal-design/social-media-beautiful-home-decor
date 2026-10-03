"""Tool wrapper: Instagram Graph API (Content Publishing) for @biancahome.

Flow: create REELS container from a public video URL → poll status_code until FINISHED
→ media_publish. Never call publish_reel without explicit human approval (CLAUDE.md rule 11).
"""
import os
import time

import httpx

GRAPH = "https://graph.facebook.com"


class InstagramError(RuntimeError):
    pass


class Instagram:
    def __init__(self, token: str | None = None, ig_user_id: str | None = None,
                 version: str | None = None, client: httpx.Client | None = None):
        self.token = token or os.environ["META_ACCESS_TOKEN"]
        self.ig_user_id = ig_user_id or os.environ["IG_USER_ID"]
        self.base = f"{GRAPH}/{version or os.environ.get('GRAPH_API_VERSION', 'v21.0')}"
        self.http = client or httpx.Client(timeout=60)

    def _call(self, method: str, path: str, **params) -> dict:
        params["access_token"] = self.token
        if method == "GET":
            resp = self.http.get(f"{self.base}/{path}", params=params)
        else:
            resp = self.http.post(f"{self.base}/{path}", data=params)
        body = resp.json()
        if resp.status_code >= 400 or "error" in body:
            err = body.get("error", {})
            raise InstagramError(f"{path}: {err.get('message', resp.text)} (code {err.get('code')})")
        return body

    def account(self) -> dict:
        return self._call("GET", self.ig_user_id, fields="username,name,followers_count,media_count")

    def publishing_limit(self) -> dict:
        return self._call("GET", f"{self.ig_user_id}/content_publishing_limit", fields="quota_usage,config")

    def create_reel_container(self, video_url: str, caption: str, share_to_feed: bool = True,
                              cover_url: str | None = None, thumb_offset_ms: int | None = None) -> str:
        params = {"media_type": "REELS", "video_url": video_url, "caption": caption,
                  "share_to_feed": str(share_to_feed).lower()}
        if cover_url:
            params["cover_url"] = cover_url
        if thumb_offset_ms is not None:
            params["thumb_offset"] = str(thumb_offset_ms)
        return self._call("POST", f"{self.ig_user_id}/media", **params)["id"]

    def wait_until_ready(self, container_id: str, timeout_s: int = 600, interval_s: int = 10) -> None:
        deadline = time.monotonic() + timeout_s
        while True:
            status = self._call("GET", container_id, fields="status_code,status")
            code = status.get("status_code")
            if code == "FINISHED":
                return
            if code in ("ERROR", "EXPIRED"):
                raise InstagramError(f"container {container_id} {code}: {status.get('status')}")
            if time.monotonic() > deadline:
                raise InstagramError(f"container {container_id} not ready after {timeout_s}s ({code})")
            time.sleep(interval_s)

    def publish(self, container_id: str) -> dict:
        media_id = self._call("POST", f"{self.ig_user_id}/media_publish", creation_id=container_id)["id"]
        return self._call("GET", media_id, fields="id,permalink,timestamp")

    def publish_reel(self, video_url: str, caption: str, **kwargs) -> dict:
        container_id = self.create_reel_container(video_url, caption, **kwargs)
        self.wait_until_ready(container_id)
        return self.publish(container_id)
