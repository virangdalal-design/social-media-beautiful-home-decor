# CLAUDE.md — Social Media Beautiful Home Decor

## Project Overview

This project is an **automated content pipeline** for creating and publishing viral social media content featuring home decor products from [Bianca Home](https://www.biancahome.com). All content is presented through the persona of **Rohan Mehta**, a witty and knowledgeable home decor influencer.

The pipeline runs daily and handles: product discovery, content generation in Rohan's voice, AI video production (with Rohan as an on-camera presenter), and multi-platform publishing — all while tracking what's been posted to avoid repetition.

**Product source:** Bianca Home (Indian online retailer — bedding, bath, dining, and home decor)
**Video generation:** SeekDance / Wavespeed / fal.ai (AI video with realistic persona)
**Target platforms:** Instagram Reels, YouTube Shorts, Facebook Reels, Twitter/X
**Persona:** Rohan Mehta — home decor influencer (see `persona/rohan-mehta.md`)

---

## Repository Structure

```
social-media-beautiful-home-decor/
├── CLAUDE.md                          # Project guide for AI assistants (this file)
│
├── persona/
│   └── rohan-mehta.md                 # Full persona definition (appearance, voice, style)
│
├── content/
│   └── {date}-{product-slug}.md       # Individual content briefs with scripts + captions
│
├── templates/
│   └── content-brief-template.md      # Template for generating new content briefs
│
├── tracking/
│   ├── content-log.csv                # Master log: every piece of content posted
│   ├── category-schedule.csv          # Category rotation tracker (7-day cooldown)
│   └── product-history.csv            # Product cooldown tracker (90-day no-repeat)
│
├── config/
│   ├── automation-rules.md            # Full automation rules and scheduling logic
│   └── api-keys.env                   # API keys (gitignored — not committed)
│
├── assets/
│   └── videos/                        # Generated video files (future)
│
└── scripts/                           # Automation scripts (future — API integrations)
```

---

## The Rohan Mehta Persona

All content is presented through **Rohan Mehta**, an AI-generated influencer character. His full definition lives in `persona/rohan-mehta.md`. Key traits:

- **Witty & funny** — Opens with bold claims, uses humor to keep viewers engaged
- **Knowledgeable** — Knows materials, brands, trends, and competitor pricing intimately
- **Honest & trustworthy** — Calls out overpriced products, only recommends what he genuinely rates
- **Relatable** — Feels like a friend sharing a great find, not a salesperson

### Rohan's Video Formula (6 Scenes, 30 seconds)
1. **THE HOOK (0-3s)** — Bold claim or price shock, mid-sentence start
2. **THE CONTEXT (3-8s)** — Why this matters, product quality callouts
3. **THE COMPETITOR SHADE (8-14s)** — Comparison to overpriced alternatives
4. **THE STYLING MOMENT (14-22s)** — Product in action, satisfying visuals
5. **THE PRICE PUNCH (22-26s)** — Dramatic price reveal with reaction
6. **THE CLOSE (26-30s)** — CTA with personality, signature sign-off

### Visual Generation
Rohan appears on camera in every video. AI video generation platforms (SeekDance, Wavespeed, fal.ai) create realistic footage of:
- Rohan speaking to camera, handling the product
- Styled room environments matching the product category
- Multiple camera angles and B-roll inserts

See `persona/rohan-mehta.md` for exact physical description, wardrobe, and on-camera direction.

---

## Product Source: Bianca Home

### Website
- **URL:** https://www.biancahome.com
- **Brand focus:** Comfort-forward home textiles and decor
- **Market:** India (prices in INR)
- **Free shipping:** Orders above Rs 999

### Product Categories

| Category | Subcategories | Social Media Potential |
|----------|--------------|----------------------|
| **Bed** | Bedsheets, Comforters, Bed-in-a-Bag, Blankets, Dohars, Pillows, Pillow Covers, Mattress Protectors | High — bedroom makeover |
| **Bath** | Towels, Bath Rugs, Shower Curtains, Bath Robes, Bath Accessories, Laundry Bags | High — bathroom aesthetic |
| **Dining & Kitchen** | Table Covers, Placemats, Kitchen items | Medium — tablescape |
| **Curtains** | Door, Long-Door, Window curtains | Medium — room transformation |
| **Decor** | Cushion Covers, Wall Clocks, Door Mats, Rugs & Carpets | High — quick refresh |
| **Lifestyle** | Bottles, Car Fragrance, Aroma products, Gift Boxes | Medium — gifting/unboxing |

### Key Collection URLs
- Bedsheets: `/collections/cotton-bed-sheets-online`
- Comforters: `/collections/buy-comforter-online`
- Towels: `/collections/soft-turkish-cotton-towel-online-with-prices`
- Bath Rugs: `/collections/bathroom-door-anti-skid-slip-mats-online`
- Cushion Covers: `/collections/printed-designer-cushion-cover-online`
- Shower Curtains: `/collections/modern-bathroom-shower-curtains-online`
- Table Covers: `/collections/round-and-rectangle-4-6-8-seater-modern-dining-table-covers`
- Curtains: `/collections/designer-living-bedroom-room-cotton-curtain-online-for-home/curtain`
- Rugs & Carpets: `/collections/living-bedroom-modern-floor-and-area-carpets-rugs-online/carpet`
- Nautica Collection: `/collections/nautica`

### Brands
- **NAUTICA** — Premium line (towels, comforters, bath accessories, bottles, wall clocks)
- **BIANCA** — House brand (bedsheets, comforters, home textiles)
- **KOPA** — Value line (microfiber comforters, bedding)
- **RUYAL** — Designer cushion covers (digital printed, silky smooth)
- **SUZANE** — Reversible silk-linen cushion covers

---

## Automation Rules (Summary)

Full rules are in `config/automation-rules.md`. Key constraints:

### Rule 1: Product Cooldown — 90 Days
No product URL may be featured more than once within 90 days. Tracked in `tracking/product-history.csv`.

### Rule 2: Category Rotation — 7 Days
No product category may repeat within 7 consecutive days. Tracked in `tracking/category-schedule.csv`. Example: if Bedsheets are featured Monday, Bedsheets cannot appear again until next Monday.

### Rule 3: New Product Priority
Products newly added to biancahome.com are prioritized over existing catalog items.

### Rule 4: Product Scoring
When multiple products are eligible, score by: discount % (30%), visual appeal (25%), newness (20%), price accessibility (15%), brand recognition (10%). Select the highest scorer.

### Rule 5: Publishing Schedule (IST)
| Platform | Time |
|----------|------|
| Instagram Reels | 7:30 PM |
| YouTube Shorts | 8:00 PM |
| Facebook Reels | 8:30 PM |
| Twitter/X | 9:00 PM |
| Instagram Stories | 9:30 PM |

### Rule 6: Content Variation
Rotate viral formulas and hook styles to keep content fresh. Never use the same hook structure twice in a row.

---

## Content Creation Workflow

### Step 1: Product Selection (Automated)
1. Scrape biancahome.com for current products and prices
2. Check `tracking/product-history.csv` — exclude products posted in last 90 days
3. Check `tracking/category-schedule.csv` — exclude categories posted in last 7 days
4. Prioritize NEW products not seen before
5. Score remaining candidates and select the best one

### Step 2: Content Brief Generation
1. Load persona from `persona/rohan-mehta.md`
2. Load template from `templates/content-brief-template.md`
3. Generate Rohan's 6-scene video script
4. Write platform-specific captions (Instagram, YouTube, Facebook, Twitter)
5. Generate hashtag sets per platform
6. Save to `content/{date}-{product-slug}.md`

### Step 3: Video Production
1. Send generation prompt to SeekDance / Wavespeed / fal.ai API
2. Include: Rohan's character description, scene breakdowns, environment, camera direction
3. Receive 30-second video (9:16, 1080x1920)
4. Add burned-in captions/subtitles
5. Save to `assets/videos/{date}-{product-slug}.mp4`

### Step 4: Multi-Platform Publishing
1. Post video + caption to Instagram Reels (via Graph API)
2. Post video + title/description to YouTube Shorts (via Data API v3)
3. Post video + caption to Facebook Reels (via Graph API)
4. Post video + tweet thread to Twitter/X (via API v2)
5. Repost to Instagram Stories with link sticker

### Step 5: Tracking Update
1. Add row to `tracking/content-log.csv` with all post URLs and details
2. Update `tracking/category-schedule.csv` with new dates
3. Update `tracking/product-history.csv` with 90-day cooldown
4. Commit tracking changes to repo

---

## Tracking System

### content-log.csv (Master Log)
Every piece of content gets a row. Columns:
```
content_id, date_published, product_name, product_category, product_subcategory,
brand, sale_price_inr, original_price_inr, discount_pct, product_url,
viral_formula, persona, instagram_posted, instagram_post_url, youtube_posted,
youtube_post_url, facebook_posted, facebook_post_url, twitter_posted,
twitter_post_url, content_file_path, video_file_path, status, notes
```

### category-schedule.csv (7-Day Rotation)
Tracks when each category was last posted and when it's eligible again:
```
category, last_posted_date, next_eligible_date, times_posted_total
```

### product-history.csv (90-Day Cooldown)
Tracks individual product URLs and their cooldown windows:
```
product_url, product_name, first_posted_date, last_posted_date, times_featured, cooldown_until
```

---

## Viral Content Formulas

Cycle through these to keep content varied:

| # | Formula | Rohan's Angle |
|---|---------|--------------|
| 1 | **Affordable Luxury Reveal** | "Someone explain to me how THIS costs Rs ___" |
| 2 | **Hidden Gem Discovery** | "Why is nobody talking about this?" |
| 3 | **Competitor Comparison** | "I'm about to make [brand] fans very angry" |
| 4 | **Before/After Transformation** | "One product. That's all it took." |
| 5 | **"Things Making My Home Look Expensive"** | Quick cuts of 3-5 affordable products |
| 6 | **ASMR / Styling Moment** | Satisfying slow-mo product arrangement |

---

## Content Guidelines

### Rohan's Voice
- Witty, warm, knowledgeable — never boring, never preachy
- Compares to competitors naturally and honestly
- Drops material/quality knowledge casually
- Uses humor to make price reveals memorable
- Mix of English with natural Hindi expressions

### Visual Aesthetic
- Clean, well-lit, styled but believable Indian homes
- Warm golden tones, soft lighting
- Product is always the visual anchor
- Multiple camera angles (medium, close-up, overhead, wide)

### Platform Behavior
- **Instagram:** Punchy, fast-paced, trending audio, 15-30s, text overlays
- **YouTube Shorts:** Slightly more detailed, SEO-optimized title, up to 60s
- **Facebook:** More descriptive caption (older demographic), engagement question at end
- **Twitter/X:** Concise tweet + thread for competitor comparison and details

### Audience
- **Primary:** Home decor enthusiasts in India (25-45 age range)
- **Secondary:** Interior design lovers, lifestyle shoppers, new homeowners
- **Psychographic:** Values aesthetics, comfort, and getting exceptional value

---

## Conventions for AI Assistants

### Daily Run Checklist
1. Check tracking CSVs before selecting a product
2. Always fetch LIVE product info from biancahome.com (prices change)
3. Generate content in Rohan's voice (load persona file)
4. Use the template for consistent structure
5. Write platform-specific content for ALL four platforms
6. Update ALL three tracking CSVs after publishing
7. Commit changes to repo

### Content File Naming
- Format: `content/{YYYY-MM-DD}-{product-slug}.md`
- Content ID: `RM-{YYYY-MM-DD}-{SEQ}` (SEQ = 001, 002, etc.)

### Writing in Rohan's Voice
- Read `persona/rohan-mehta.md` before writing any content
- Hook lines must be bold, funny, or shocking — never generic
- Include competitor shade (Rohan always explains why others charge more)
- Price reveal must feel dramatic — build anticipation
- Closing must feel personal with a signature touch

### Video Generation Prompts
- Always include Rohan's physical description from the persona file
- Describe environment, lighting, camera movements per scene
- Specify 9:16 vertical, 1080x1920, 30fps
- Include audio layer notes (voice tone, music style, SFX)

### Quality Checklist
Before finalizing any content piece, verify:
- [ ] Hook is in Rohan's voice and stops the scroll
- [ ] Competitor comparison is included and feels natural
- [ ] Price reveal has a dramatic build-up
- [ ] Captions written for ALL four platforms
- [ ] Hashtag sets are platform-appropriate and diverse
- [ ] Video script has 6 scenes with timing markers
- [ ] SeekDance prompt includes character + environment + camera direction
- [ ] Product details (price, name, URL) are verified as current
- [ ] Tracking CSVs checked — no 90-day or 7-day violations
- [ ] Content file saved with correct naming convention

---

## API Integration (Awaiting Keys)

### Video Generation
```
Providers: SeekDance, Wavespeed (queue.fal), fal.ai
Config location: config/api-keys.env (gitignored)
Input: Character prompt + scene descriptions + audio specs
Output: MP4, 9:16, 1080x1920, 30 seconds
```

### Social Media Publishing
```
Instagram: Graph API (Business account) — Reels + Stories
YouTube: Data API v3 — Shorts upload
Facebook: Graph API — Reels upload
Twitter/X: API v2 — Tweets with media upload
Config location: config/api-keys.env (gitignored)
```

User will provide API keys when ready. Scripts will be developed in `scripts/` directory.

---

## Tools & Services

| Tool | Purpose | URL |
|------|---------|-----|
| Bianca Home | Product source & imagery | https://www.biancahome.com |
| SeekDance | AI video generation (primary) | https://seekdance.com |
| Wavespeed/fal.ai | AI video generation (fallback) | https://fal.ai |
| Instagram | Publishing — Reels + Stories | https://www.instagram.com |
| YouTube | Publishing — Shorts | https://www.youtube.com |
| Facebook | Publishing — Reels | https://www.facebook.com |
| Twitter/X | Publishing — Tweets | https://x.com |

---

## Development Notes

- Content batches are organized by date (one product per day)
- Tracking CSVs are the source of truth for scheduling — always check before creating content
- The 90-day product cooldown and 7-day category rotation are non-negotiable rules
- When API keys are provided, build integration scripts in `scripts/`
- Monitor engagement metrics to refine the product scoring algorithm
- Iterate on Rohan's persona based on which content performs best
