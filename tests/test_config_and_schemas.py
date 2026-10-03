import json
from pathlib import Path

import jsonschema
import yaml

from bianca_studio.config import ROOT, delivery_spec, load_models, pick_video_model, pick_video_models


def test_every_purpose_has_final_tier_models():
    tiers = load_models()["video"]["tiers"]
    for purpose in ("final", "human_motion", "product_macro", "cinematic"):
        assert tiers[purpose], purpose
        assert pick_video_model(purpose)["model"]


def test_best_of_returns_top_n():
    assert len(pick_video_models("final")) == load_models()["video"]["defaults"]["best_of"]
    assert pick_video_models("final", n=1)[0] == pick_video_model("final")


def test_quality_first_defaults():
    m = load_models()
    assert m["video"]["defaults"]["draft_first"] is False
    assert m["qc"]["pass_threshold"] >= 85


def test_delivery_spec_is_instagram_reel():
    s = delivery_spec()
    assert (s["width"], s["height"]) == (1080, 1920)
    assert 23 <= s["fps"] <= 60 and s["max_size_mb"] <= 100


def test_schemas_are_valid_and_brief_example_validates():
    for p in (ROOT / "schemas").glob("*.json"):
        jsonschema.Draft202012Validator.check_schema(json.loads(p.read_text()))
    brief = {
        "product_id": "bedsheet-aurora-king", "name": "Aurora Printed Cotton Bedsheet Set",
        "brand": "Bianca Home", "category": "bedding",
        "product_url": "https://www.biancahome.com/products/x", "description": "d",
        "material": "100% cotton, 210 TC", "size_contents": "King + 2 pillow covers",
        "print_or_colour": "Aurora sage", "logo_notes": "label bottom-left",
        "selling_points": ["a", "b", "c"], "audience": "28-45 urban India",
        "price_point": "₹1,799", "photos": [f"https://x.test/{i}.jpg" for i in range(6)],
        "platform": "instagram_reel", "target_duration_s": 15,
    }
    jsonschema.validate(brief, json.loads((ROOT / "schemas/product_brief.json").read_text()))


def test_presenters_registry_matches_bibles():
    reg = yaml.safe_load((ROOT / "docs/characters/presenters.yaml").read_text())["presenters"]
    assert {p["angle"] for p in reg} == {"informative", "aspirational", "fun", "luxury"}
    for p in reg:
        assert Path(ROOT / p["bible"]).exists(), p["bible"]
    rohan = next(p for p in reg if p["id"] == "rohan")
    assert "Nautica" not in rohan["brands"]


def test_comparison_lane_never_reaches_router():
    m = load_models()
    assert "comparison" not in m["video"]["tiers"]
    cheap = {c["model"] for c in m["comparison"]["video"]}
    routed = {c["model"] for name, tier in m["video"]["tiers"].items() if name != "draft" for c in tier}
    assert not cheap & routed
