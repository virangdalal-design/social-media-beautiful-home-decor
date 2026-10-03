# Automation Rules — Daily Content Agent

## Overview

This document defines the rules the automated content agent follows when triggered daily. The agent selects a product, generates content in Rohan Mehta's voice, produces a video via AI video generation, and publishes across all platforms.

---

## Daily Trigger Flow

```
1. PRODUCT SELECTION
   ├── Scrape biancahome.com for current products and prices
   ├── Check tracking/product-history.csv → exclude products posted in last 90 days
   ├── Check tracking/category-schedule.csv → exclude categories posted in last 7 days
   ├── Prioritize NEW products (not seen in previous scrapes)
   ├── Score remaining products by viral potential (discount %, visual appeal, trend fit)
   └── Select top candidate

2. CONTENT GENERATION
   ├── Load persona from persona/rohan-mehta.md
   ├── Generate content brief using templates/content-brief-template.md
   ├── Write video script (Rohan's 6-scene formula)
   ├── Write platform-specific captions (Instagram, YouTube, Facebook, Twitter)
   ├── Generate hashtag sets per platform
   └── Save content brief to content/{date}-{product-slug}.md

3. VIDEO PRODUCTION
   ├── Send prompt to SeekDance / Wavespeed / fal.ai API
   ├── Include: character description, environment, camera direction, audio notes
   ├── Receive video file (9:16, 1080x1920, 30 seconds)
   ├── Add captions/subtitles to video (burned in)
   └── Save video to assets/videos/{date}-{product-slug}.mp4

4. PUBLISHING
   ├── Post to Instagram Reels (7:30 PM IST)
   ├── Post to YouTube Shorts (8:00 PM IST)
   ├── Post to Facebook Reels (8:30 PM IST)
   ├── Post to Twitter/X (9:00 PM IST)
   ├── Repost to Instagram Stories with link sticker (9:30 PM IST)
   └── Update tracking CSVs with post URLs and status

5. TRACKING UPDATE
   ├── Update tracking/content-log.csv with full record
   ├── Update tracking/category-schedule.csv with new dates
   ├── Update tracking/product-history.csv with cooldown
   └── Commit and push tracking updates to repo
```

---

## Rule 1: Product Cooldown (90 Days)

**No product may be featured more than once within 90 days.**

### Implementation
- Before selecting a product, check `tracking/product-history.csv`
- Compare `product_url` against current candidates
- If `cooldown_until` > today's date → SKIP this product
- After posting, set `cooldown_until` = today + 90 days

### Exceptions
- A product may be re-featured early ONLY if:
  - It has a new significant price drop (>20% further reduction)
  - It has new color variants not previously covered
  - Manual override is explicitly set

---

## Rule 2: Category Rotation (7 Days)

**No product category may be featured more than once within 7 consecutive days.**

### Implementation
- Before selecting a product, check `tracking/category-schedule.csv`
- If `next_eligible_date` > today's date → SKIP this category
- After posting, update:
  - `last_posted_date` = today
  - `next_eligible_date` = today + 7 days
  - `times_posted_total` += 1

### Category Mapping

| Category (in CSV) | Products Included |
|-------------------|-------------------|
| Bedsheets | All bedsheets (king, double, single) |
| Comforters | Comforters, bed-in-a-bag, dohars |
| Blankets | Blankets of all types |
| Pillows | All pillow types |
| Pillow Covers | Pillow covers |
| Towels | Bath towels, hand towels, face towels |
| Bath Rugs | Bath mats, bath rugs |
| Shower Curtains | Shower curtains |
| Bath Accessories | Trays, toothbrush holders, soap dispensers |
| Bath Robes | Robes |
| Table Covers | Table covers, tablecloths |
| Placemats | Placemats, runners |
| Curtains | All curtain types (door, window, long-door) |
| Cushion Covers | All cushion cover brands (Ruyal, Suzane, Bianca) |
| Wall Clocks | Wall clocks |
| Door Mats | Door mats |
| Rugs & Carpets | Area rugs, carpets |
| Bottles | Water bottles, flasks |
| Car Fragrance | Car fragrances, air fresheners |
| Aroma | Aroma products, diffusers |
| Gift Boxes | Gift sets, curated boxes |

---

## Rule 3: New Product Priority

**Products newly added to biancahome.com should be prioritized over existing catalog items.**

### Implementation
- Maintain a product catalog snapshot (optional: `tracking/catalog-snapshot.json`)
- On each run, compare current website products with last known catalog
- New products (not in previous snapshot) get a priority boost in scoring
- "New" products that are also on deep discount (>50% off) get highest priority

---

## Rule 4: Product Scoring

**When multiple eligible products exist, score them to pick the best candidate.**

| Factor | Weight | Scoring |
|--------|--------|---------|
| Discount percentage | 30% | >80% = 10, >60% = 8, >40% = 6, >20% = 4, <20% = 2 |
| Visual appeal (category) | 25% | Decor/Bath Acc = 10, Bed/Bath = 8, Curtains = 6, Kitchen = 5, Lifestyle = 4 |
| Is new product | 20% | Yes = 10, No = 3 |
| Price point (accessibility) | 15% | <500 = 10, <1000 = 8, <2000 = 6, <5000 = 4, >5000 = 2 |
| Brand recognition | 10% | NAUTICA = 10, BIANCA = 7, SUZANE = 6, RUYAL = 5, KOPA = 4 |

### Scoring Formula
```
score = (discount * 0.30) + (visual * 0.25) + (new * 0.20) + (price * 0.15) + (brand * 0.10)
```

Select the product with the highest score. In case of tie, prefer the newer product.

---

## Rule 5: Publishing Schedule

### Time Slots (IST — Indian Standard Time)

| Platform | Time | Rationale |
|----------|------|-----------|
| Instagram Reels | 7:30 PM | Peak engagement window for Indian audience |
| YouTube Shorts | 8:00 PM | Catch evening browsing wave |
| Facebook Reels | 8:30 PM | Older demographic scrolls slightly later |
| Twitter/X | 9:00 PM | Twitter engagement peaks late evening |
| Instagram Stories | 9:30 PM | Repost Reel for additional reach |

### Day Selection
- **Prefer:** Wednesday, Thursday, Sunday (highest home decor engagement)
- **Avoid:** Saturday (lower engagement for shopping content)
- **Daily run is fine** — the category rotation rule prevents repetitiveness

---

## Rule 6: Content Variation

**Even with the same viral formula, vary the execution to keep content fresh.**

### Rotation of Viral Formulas
Cycle through these in order, then repeat:
1. Affordable Luxury Reveal
2. Hidden Gem Discovery
3. Competitor Comparison
4. Before/After Transformation
5. "Things Making My Home Look Expensive"
6. ASMR / Styling Moment

### Rohan's Opening Hooks — Variety
Never use the same hook structure twice in a row. Rotate between:
- Price shock: "Rs ___ for THIS?"
- Bold claim: "This product just ended the overpriced [category] market."
- Question: "Why is nobody talking about this?"
- Story: "So I was browsing Bianca Home at 2 AM and..."
- Challenge: "Find me a better [product] for under Rs ___. I'll wait."
- Controversy: "I'm about to make [competitor brand] fans very angry."

---

## API Integration Points

### Video Generation (awaiting API keys)
```
Provider options:
- SeekDance API (primary)
- Wavespeed queue.fal (fallback)
- fal.ai (fallback)

Required per call:
- Character prompt (from persona/rohan-mehta.md)
- Scene descriptions (from content brief)
- Audio/voice specifications
- Output format: MP4, 9:16, 1080x1920, 30s
```

### Social Media Publishing (awaiting API keys)
```
Instagram:
- Instagram Graph API / Business API
- Required: access_token, page_id
- Endpoint: Reels upload, Stories upload

YouTube:
- YouTube Data API v3
- Required: OAuth2 credentials
- Endpoint: Videos.insert (shorts)

Facebook:
- Facebook Graph API
- Required: access_token, page_id
- Endpoint: Video upload, Reels

Twitter/X:
- Twitter API v2
- Required: OAuth2 bearer token
- Endpoint: Tweets with media
```

### Configuration File (to be created when API keys are provided)
```
config/
├── api-keys.env          # API keys (gitignored)
├── automation-rules.md   # This file
└── platform-config.json  # Platform-specific settings
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No eligible product found (all on cooldown) | Skip day, log warning, notify |
| Video generation API fails | Retry 3x with backoff, then skip video and post image carousel instead |
| Social media API fails | Retry 3x, log failure, mark as "failed" in tracking CSV |
| Product price changed since selection | Re-fetch price, update content if >10% change |
| Product out of stock | Skip product, select next candidate, log skip reason |

---

## File Outputs Per Run

Each daily execution produces:
1. `content/{date}-{product-slug}.md` — Full content brief
2. `assets/videos/{date}-{product-slug}.mp4` — Generated video (when API connected)
3. Updated `tracking/content-log.csv` — New row with all details
4. Updated `tracking/category-schedule.csv` — Category dates refreshed
5. Updated `tracking/product-history.csv` — Product cooldown set
