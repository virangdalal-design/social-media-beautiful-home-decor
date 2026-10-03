"""
Product-to-Instagram Content Pipeline

Full workflow:
  1. Scrape product details from biancahome.com
  2. Generate Instagram content (captions, hashtags, CTAs)
  3. Generate video via Seedance API
  4. Post Reel to Instagram via Graph API

Usage:
  python pipeline.py scrape <product_url>
  python pipeline.py generate-video <content_dir>
  python pipeline.py post-instagram <content_dir>
  python pipeline.py full <product_url>
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEEDANCE_API_URL = os.getenv("SEEDANCE_API_URL", "https://kie.ai/api/bytedance/v1-lite-text-to-video")
SEEDANCE_API_KEY = os.getenv("SEEDANCE_API_KEY", "")

INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v21.0")

CONTENT_DIR = Path("content")


# ---------------------------------------------------------------------------
# Step 1: Scrape product from biancahome.com
# ---------------------------------------------------------------------------

def scrape_product(product_url: str) -> dict:
    """Scrape product details from a biancahome.com product page."""
    print(f"[1/4] Scraping product: {product_url}")

    resp = requests.get(product_url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract JSON-LD structured data if available
    product_data = {}
    ld_json = soup.find("script", {"type": "application/ld+json"})
    if ld_json:
        try:
            ld = json.loads(ld_json.string)
            if isinstance(ld, list):
                for item in ld:
                    if item.get("@type") == "Product":
                        ld = item
                        break
            if ld.get("@type") == "Product":
                product_data = {
                    "product_name": ld.get("name", ""),
                    "brand": ld.get("brand", {}).get("name", "") if isinstance(ld.get("brand"), dict) else str(ld.get("brand", "")),
                    "description": ld.get("description", ""),
                    "sku": ld.get("sku", ""),
                    "price": {
                        "sale": float(ld.get("offers", {}).get("price", 0)),
                        "currency": ld.get("offers", {}).get("priceCurrency", "INR"),
                    },
                    "product_url": product_url,
                    "source_website": "https://www.biancahome.com",
                }
        except (json.JSONDecodeError, AttributeError):
            pass

    # Fallback: parse from HTML
    if not product_data.get("product_name"):
        title_el = soup.find("h1")
        product_data["product_name"] = title_el.get_text(strip=True) if title_el else "Unknown Product"

    # Extract images
    images = []
    for img in soup.select("img[src*='/cdn/shop/']"):
        src = img.get("src", "")
        if src and src not in images:
            images.append(src if src.startswith("http") else f"https://www.biancahome.com{src}")
    product_data["images"] = images[:6]

    # Save to content directory
    slug = urlparse(product_url).path.strip("/").split("/")[-1].replace("_", "-")
    out_dir = CONTENT_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "product_info.json"
    product_data["scraped_date"] = time.strftime("%Y-%m-%d")
    with open(out_file, "w") as f:
        json.dump(product_data, f, indent=2)

    print(f"    Saved product info -> {out_file}")
    return product_data


# ---------------------------------------------------------------------------
# Step 2: Generate Instagram content
# ---------------------------------------------------------------------------

def generate_content(product: dict, content_dir: Path) -> dict:
    """Generate Instagram captions, hashtags, and SeekDance prompt from product data."""
    print("[2/4] Generating Instagram content...")

    name = product.get("product_name", "Home Decor Product")
    brand = product.get("brand", "")
    description = product.get("description", "")
    features = product.get("features", [])
    price_info = product.get("price", {})

    feature_text = ", ".join(features[:3]) if features else "premium quality"
    price_text = ""
    if price_info.get("sale"):
        price_text = f"Now at Rs {int(price_info['sale']):,}"

    content = {
        "product_name": name,
        "platform": "Instagram",
        "format": "Reel",
        "content_created": time.strftime("%Y-%m-%d"),

        "caption_short": (
            f"Elevate your space with the {name}. "
            f"Crafted with {feature_text} — designed for those who appreciate the finer things. "
            f"Your home deserves this."
        ),

        "caption_extended": (
            f"Every detail matters when you're creating a space that feels like home. "
            f"The {name} by {brand} brings together quality craftsmanship and timeless style. "
            f"{description[:200] + '...' if len(description) > 200 else description}\n\n"
            f"{price_text + '. ' if price_text else ''}"
            f"Because your home should feel as beautiful as it looks."
        ),

        "hashtags": [
            "#homedecor", "#interiordesign", "#bedroomdecor",
            f"#{brand.lower().replace(' ', '')}" if brand else "#homedesign",
            "#biancahome", "#luxurybedding", "#cozyhome",
            "#homeinspo", "#bedroomaesthetic", "#luxuryliving",
            "#homestyle", "#minimaldecor", "#softliving",
            "#bedroominspo", "#homedecorinspo",
        ],

        "call_to_action": "Shop now — link in bio. Transform your space today.",

        "seekdance_prompt": (
            f"A cinematic home decor scene showcasing a luxurious {name}. "
            f"Soft golden morning light filters through sheer curtains into a styled modern bedroom. "
            f"The camera slowly pans across the product, revealing its premium texture and craftsmanship. "
            f"Close-up of the fabric texture catching the light. "
            f"Wide shot of the beautifully styled room with the product as the centerpiece. "
            f"Clean, minimal aesthetic. Aspirational lifestyle commercial style. 9:16 vertical format."
        ),

        "posting_schedule": {
            "best_times": ["9:00 AM", "12:00 PM", "7:00 PM"],
            "best_days": ["Tuesday", "Wednesday", "Thursday"],
            "timezone": "IST (Asia/Kolkata)",
        },
    }

    out_file = content_dir / "instagram_content.json"
    with open(out_file, "w") as f:
        json.dump(content, f, indent=2)

    print(f"    Caption: {content['caption_short'][:80]}...")
    print(f"    Hashtags: {len(content['hashtags'])} tags")
    print(f"    Saved content -> {out_file}")
    return content


# ---------------------------------------------------------------------------
# Step 3: Generate video via Seedance
# ---------------------------------------------------------------------------

def generate_video(content_dir: Path) -> str | None:
    """Submit a video generation request to the Seedance API."""
    print("[3/4] Generating video via Seedance...")

    content_file = content_dir / "instagram_content.json"
    if not content_file.exists():
        print(f"    ERROR: {content_file} not found. Run content generation first.")
        return None

    with open(content_file) as f:
        content = json.load(f)

    prompt = content.get("seekdance_prompt", "")
    if not prompt:
        print("    ERROR: No SeekDance prompt found in content.")
        return None

    if not SEEDANCE_API_KEY:
        print("    WARNING: SEEDANCE_API_KEY not set. Saving prompt for manual use.")
        prompt_file = content_dir / "seedance_prompt.txt"
        with open(prompt_file, "w") as f:
            f.write(prompt)
        print(f"    Saved prompt -> {prompt_file}")
        print(f"    Use this prompt at https://seedance.io or via the Seedance API.")
        return None

    # Submit video generation request
    headers = {
        "Authorization": f"Bearer {SEEDANCE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "resolution": "1080p",
        "aspect_ratio": "9:16",
        "duration": 15,
    }

    resp = requests.post(SEEDANCE_API_URL, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    result = resp.json()

    task_id = result.get("task_id") or result.get("id", "")
    print(f"    Video generation submitted. Task ID: {task_id}")

    # Poll for completion
    status_url = result.get("status_url", f"{SEEDANCE_API_URL}/status/{task_id}")
    video_url = poll_video_status(status_url, headers)

    if video_url:
        # Download the video
        video_file = content_dir / "reel_video.mp4"
        download_file(video_url, video_file)
        print(f"    Video saved -> {video_file}")

        # Update content with video URL
        content["video_url"] = video_url
        content["video_file"] = str(video_file)
        with open(content_file, "w") as f:
            json.dump(content, f, indent=2)

        return str(video_file)

    print("    WARNING: Video generation still processing. Check back later.")
    return None


def poll_video_status(status_url: str, headers: dict, max_attempts: int = 30, interval: int = 10) -> str | None:
    """Poll the Seedance API until video is ready."""
    for attempt in range(max_attempts):
        time.sleep(interval)
        try:
            resp = requests.get(status_url, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status", "").lower()
            if status in ("completed", "success", "done"):
                return data.get("video_url") or data.get("output_url", "")
            if status in ("failed", "error"):
                print(f"    ERROR: Video generation failed: {data.get('message', 'Unknown error')}")
                return None
            print(f"    Status: {status} (attempt {attempt + 1}/{max_attempts})")
        except requests.RequestException as e:
            print(f"    Polling error: {e}")
    return None


def download_file(url: str, dest: Path):
    """Download a file from a URL."""
    resp = requests.get(url, stream=True, timeout=120)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


# ---------------------------------------------------------------------------
# Step 4: Post to Instagram
# ---------------------------------------------------------------------------

def post_to_instagram(content_dir: Path) -> str | None:
    """Post a Reel to Instagram using the Graph API."""
    print("[4/4] Posting to Instagram...")

    if not INSTAGRAM_ACCESS_TOKEN or not INSTAGRAM_USER_ID:
        print("    ERROR: INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_USER_ID must be set.")
        print("    Set these in your .env file. See .env.example for details.")
        return None

    content_file = content_dir / "instagram_content.json"
    if not content_file.exists():
        print(f"    ERROR: {content_file} not found.")
        return None

    with open(content_file) as f:
        content = json.load(f)

    video_url = content.get("video_url")
    if not video_url:
        print("    ERROR: No video_url in content. Generate video first.")
        return None

    caption = content["caption_short"]
    hashtags = " ".join(content["hashtags"])
    cta = content.get("call_to_action", "")
    full_caption = f"{caption}\n\n{cta}\n\n{hashtags}"

    base_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{INSTAGRAM_USER_ID}"

    # Step 1: Create media container
    print("    Creating media container...")
    container_resp = requests.post(
        f"{base_url}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": full_caption,
            "share_to_feed": "true",
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=60,
    )
    container_resp.raise_for_status()
    container_id = container_resp.json().get("id")
    print(f"    Container created: {container_id}")

    # Step 2: Wait for processing
    print("    Waiting for Instagram to process the video...")
    for attempt in range(30):
        time.sleep(10)
        status_resp = requests.get(
            f"https://graph.facebook.com/{GRAPH_API_VERSION}/{container_id}",
            params={
                "fields": "status_code",
                "access_token": INSTAGRAM_ACCESS_TOKEN,
            },
            timeout=30,
        )
        status = status_resp.json().get("status_code", "")
        if status == "FINISHED":
            break
        if status == "ERROR":
            print(f"    ERROR: Instagram video processing failed.")
            return None
        print(f"    Processing... ({status}, attempt {attempt + 1}/30)")

    # Step 3: Publish
    print("    Publishing Reel...")
    publish_resp = requests.post(
        f"{base_url}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=60,
    )
    publish_resp.raise_for_status()
    media_id = publish_resp.json().get("id")
    print(f"    Published! Media ID: {media_id}")

    # Save result
    result = {
        "media_id": media_id,
        "container_id": container_id,
        "published_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "caption": full_caption,
    }
    with open(content_dir / "post_result.json", "w") as f:
        json.dump(result, f, indent=2)

    return media_id


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Product-to-Instagram Content Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # scrape
    p_scrape = sub.add_parser("scrape", help="Scrape product details from biancahome.com")
    p_scrape.add_argument("product_url", help="Full URL of the product page")

    # generate-video
    p_video = sub.add_parser("generate-video", help="Generate video via Seedance API")
    p_video.add_argument("content_dir", help="Path to content directory")

    # post-instagram
    p_post = sub.add_parser("post-instagram", help="Post Reel to Instagram")
    p_post.add_argument("content_dir", help="Path to content directory")

    # full pipeline
    p_full = sub.add_parser("full", help="Run the full pipeline end-to-end")
    p_full.add_argument("product_url", help="Full URL of the product page")

    args = parser.parse_args()

    if args.command == "scrape":
        product = scrape_product(args.product_url)
        slug = urlparse(args.product_url).path.strip("/").split("/")[-1].replace("_", "-")
        content_dir = CONTENT_DIR / slug
        generate_content(product, content_dir)

    elif args.command == "generate-video":
        generate_video(Path(args.content_dir))

    elif args.command == "post-instagram":
        post_to_instagram(Path(args.content_dir))

    elif args.command == "full":
        product = scrape_product(args.product_url)
        slug = urlparse(args.product_url).path.strip("/").split("/")[-1].replace("_", "-")
        content_dir = CONTENT_DIR / slug
        generate_content(product, content_dir)
        video_file = generate_video(content_dir)
        if video_file:
            post_to_instagram(content_dir)
        else:
            print("\nVideo not ready yet. Once you have it, run:")
            print(f"  python pipeline.py post-instagram {content_dir}")


if __name__ == "__main__":
    main()
