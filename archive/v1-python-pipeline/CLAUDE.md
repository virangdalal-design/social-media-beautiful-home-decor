# CLAUDE.md — Social Media Beautiful Home Decor

## Project Overview

This project automates and streamlines the creation of social media content for beautiful home decor products. The workflow involves:

1. **Product Selection** — Browse and select products from [Bianca Home](https://www.biancahome.com)
2. **Content Creation** — Generate marketing copy, captions, hashtags, and visual descriptions around selected products
3. **Video Production** — Produce short-form video content using [SeekDance](https://seekdance.com) (AI video generation)
4. **Social Media Publishing** — Post finished content to Instagram (and potentially other platforms)

## Repository Structure

```
social-media-beautiful-home-decor/
├── CLAUDE.md                    # This file — project guide for AI assistants
├── pipeline.py                  # Full pipeline script (scrape → content → video → post)
├── requirements.txt             # Python dependencies
├── .env.example                 # API keys template (copy to .env and fill in)
├── .gitignore
└── content/                     # Generated content organized by product
    └── <product-slug>/
        ├── product_info.json    # Scraped product details
        ├── instagram_content.json  # Captions, hashtags, CTA, video prompt
        └── seedance_prompt.txt  # Standalone video generation prompt
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy .env.example to .env and fill in your API keys
cp .env.example .env

# 3. Run the full pipeline for a product
python pipeline.py full "https://www.biancahome.com/products/..."

# Or run individual steps:
python pipeline.py scrape "https://www.biancahome.com/products/..."
python pipeline.py generate-video content/<product-slug>
python pipeline.py post-instagram content/<product-slug>
```

## Workflow Details

### Step 1: Product Selection (Bianca Home)

- Source: https://www.biancahome.com
- Select products that are visually appealing and suitable for social media promotion
- Capture key product details: name, description, price, images, product URL
- Focus categories: home decor, textiles, furnishings, accessories

### Step 2: Content Generation

For each selected product, create:

- **Short caption** — Engaging Instagram caption (1-3 sentences)
- **Extended description** — Longer-form content for carousel posts or stories
- **Hashtags** — Relevant hashtags for reach (e.g., #homedecor #interiordesign #biancahome)
- **Call to action** — Drive engagement or traffic (e.g., "Link in bio", "Shop now")
- **Visual notes** — Describe the aesthetic, mood, and styling for video production

### Step 3: Video Production (SeekDance)

- Platform: SeekDance (AI-powered video generation)
- Input: Product images, descriptions, and visual notes from Step 2
- Output: Short-form video (15-60 seconds) optimized for Instagram Reels
- Style: Clean, aesthetic, lifestyle-oriented home decor visuals

### Step 4: Instagram Publishing

- Format: Reels, carousel posts, or stories
- Include caption, hashtags, and product tags
- Optimal posting times and engagement strategies should be considered
- Tag @biancahome or relevant brand accounts where appropriate

## Content Guidelines

- **Tone**: Aspirational, warm, inviting — lifestyle-focused rather than hard-sell
- **Aesthetic**: Clean, minimal, well-lit — consistent with modern home decor trends
- **Audience**: Home decor enthusiasts, interior design lovers, lifestyle-oriented shoppers
- **Platform focus**: Instagram (Reels, Feed, Stories)

## Conventions for AI Assistants

- When selecting products, prioritize items with strong visual appeal and clear lifestyle application
- Generated captions should feel authentic and human — avoid overly salesy language
- Hashtag sets should mix high-volume tags (#homedecor) with niche tags (#biancahome #luxuryliving)
- All content should be original and not copy product descriptions verbatim
- When producing video prompts for SeekDance, be specific about camera movements, transitions, and mood
- Keep Instagram Reels content between 15-30 seconds for optimal engagement
- Always include a clear call-to-action in captions

## Tools & Services

| Tool | Purpose | URL |
|------|---------|-----|
| Bianca Home | Product source | https://www.biancahome.com |
| Seedance | AI video generation (by ByteDance) | https://seedance.io |
| Instagram Graph API | Publishing platform | https://developers.facebook.com/docs/instagram-api/ |

## API Setup

### Seedance (Video Generation)
- Sign up at https://seedance.io or https://kie.ai
- Get an API key for text-to-video generation
- Supports 480p/720p/1080p, multiple aspect ratios, 5-15 second videos

### Instagram Graph API
- Requires a Meta Developer App and Instagram Business Account
- Need `instagram_content_publish` permission
- Uses two-step container model: create container → wait for processing → publish
- Video must be publicly accessible URL for the Reels upload

## Development Notes

- This repository tracks content plans, generated assets, and workflow automation
- Content batches can be organized by date or campaign
- Keep product selections and generated content versioned for iteration
- Video files (.mp4) are gitignored — only prompts and metadata are versioned
