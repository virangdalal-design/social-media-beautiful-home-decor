import httpx
import pytest

from bianca_studio.tools import instagram as ig_mod
from bianca_studio.tools.instagram import Instagram, InstagramError


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_publish_reel_happy_path(monkeypatch):
    monkeypatch.setattr(ig_mod.time, "sleep", lambda s: None)
    calls = []
    statuses = iter(["IN_PROGRESS", "FINISHED"])

    def handler(req: httpx.Request):
        calls.append((req.method, req.url.path))
        if req.url.path.endswith("/123/media"):
            body = dict(httpx.QueryParams(req.content.decode()))
            assert body["media_type"] == "REELS" and body["video_url"] == "https://cdn/x.mp4"
            return httpx.Response(200, json={"id": "c1"})
        if req.url.path.endswith("/c1"):
            return httpx.Response(200, json={"status_code": next(statuses)})
        if req.url.path.endswith("/media_publish"):
            return httpx.Response(200, json={"id": "m1"})
        if req.url.path.endswith("/m1"):
            return httpx.Response(200, json={"id": "m1", "permalink": "https://instagram.com/reel/abc"})
        raise AssertionError(req.url)

    ig = Instagram(token="t", ig_user_id="123", version="v21.0", client=_client(handler))
    media = ig.publish_reel("https://cdn/x.mp4", "caption")
    assert media["permalink"].endswith("/abc")
    assert [p for _, p in calls][-2:] == ["/v21.0/123/media_publish", "/v21.0/m1"]


def test_container_error_raises(monkeypatch):
    monkeypatch.setattr(ig_mod.time, "sleep", lambda s: None)

    def handler(req):
        if req.url.path.endswith("/media"):
            return httpx.Response(200, json={"id": "c1"})
        return httpx.Response(200, json={"status_code": "ERROR", "status": "bad codec"})

    ig = Instagram(token="t", ig_user_id="123", client=_client(handler))
    with pytest.raises(InstagramError, match="bad codec"):
        ig.publish_reel("https://cdn/x.mp4", "c")


def test_graph_error_surfaces_message():
    def handler(req):
        return httpx.Response(400, json={"error": {"message": "Invalid OAuth access token", "code": 190}})

    ig = Instagram(token="t", ig_user_id="123", client=_client(handler))
    with pytest.raises(InstagramError, match="Invalid OAuth"):
        ig.account()
