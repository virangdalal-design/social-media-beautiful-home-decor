# 00 — Setup: accounts, purchases, keys

Everything that has to exist before the first paid generation. Work top to bottom.
When done, put the values in `config/.env` (copy of `config/.env.example`, never committed)
and run:

```bash
make setup
python -m bianca_studio.cli doctor
```

`doctor` checks every key is present and makes one free, read-only call per service.
All green = Phase 0 gate is half done (the other half is a test Reel, see the end).

Prices are what providers listed around Sep–Oct 2026; confirm on the pricing page when
you buy. ₹ at ~₹88/$.

---

## A. Needed now (Track A — brand videos)

| # | Service | What for | Buy | Approx. cost | Env vars |
|---|---|---|---|---|---|
| 1 | **fal.ai** | One gateway for all top video + image + upscale models (Seedance 2.5, Kling O3/3.0, Veo 3.1, Nano Banana, Topaz) | Prepaid credits | Start with **$200 (₹17,600)** for Phase 1 | `FAL_KEY` |
| 2 | **Google AI Studio (Gemini API)** | QC agent (watches video), Nano Banana direct fallback | Pay-as-you-go, billing on | ~$10–20/month | `GOOGLE_API_KEY` |
| 3 | **Anthropic API** | Strategist / Director / Producer agents (Phase 2). Phase 1 runs in Claude Code by hand. | Pay-as-you-go | ~$10–30/month | `ANTHROPIC_API_KEY` |
| 4 | **Supabase** | Database + storage. Instagram needs a public URL to fetch the video from. | Pro plan once storage > 1 GB | Free → $25/month | `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_STORAGE_BUCKET` |
| 5 | **Meta (Instagram Graph API)** | Publishing to @biancahome | Free | ₹0 | `META_ACCESS_TOKEN`, `IG_USER_ID`, `GRAPH_API_VERSION` |
| 6 | **Music licence** | Background music cleared for brand/commercial use on Instagram | Epidemic Sound or Artlist **business** plan; or free Meta Sound Collection | Free → ~$20/month | none (files go in assets/music/) |
| 7 | **ElevenLabs** (optional) | Voice-over, if a video uses narration | Creator plan | ~$22/month | `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` |

Not needed now: Higgsfield (Track B identity), Railway (Phase 2 approval page), Blotato (Phase 3).

### Budget to get to the Phase 1 gate
| Item | ₹ | $ |
|---|---|---|
| fal.ai credits (expect 30–60 clip attempts at top tier) | 17,600 | 200 |
| Gemini + Anthropic usage | 2,500 | 30 |
| Music licence (1 month) | 0–1,800 | 0–20 |
| ElevenLabs (1 month, optional) | 0–1,950 | 0–22 |
| **Total** | **~20,000–24,000** | **~230–270** |

Expected steady-state cost (Phase 2+) per finished, approved 15s video at top-tier
models: **₹3,500–7,000 ($40–80)**, falling as prompts mature and first-try hit-rate rises.
This is deliberately higher than the original ₹300–600 estimate: top models at 1080p/4K
cost ~$0.40–1.15 per generated second, and we keep the best of several takes.

---

## B. Step-by-step

### 1. fal.ai
1. Sign up at https://fal.ai with the Bianca business email.
2. Billing → add card → buy $200 credits. Turn on a usage alert at $150.
3. Dashboard → Keys → create key `bianca-studio` → copy to `FAL_KEY`.
4. In the model gallery, open each model listed in `config/models.yaml` and confirm the
   endpoint id. Fix the ids in `config/models.yaml` if fal has renamed them.

### 2. Google AI Studio (Gemini)
1. https://aistudio.google.com → Get API key → create in a new Google Cloud project
   `bianca-studio`.
2. Enable billing on that project (free tier limits are too low for video QC).
3. Copy to `GOOGLE_API_KEY`.

### 3. Anthropic
1. https://console.anthropic.com → Billing → add $25 credit.
2. API keys → create `bianca-studio` → `ANTHROPIC_API_KEY`.

### 4. Supabase
1. https://supabase.com → New project `bianca-studio`, region **Mumbai (ap-south-1)**.
2. Project Settings → API → copy Project URL → `SUPABASE_URL`, `service_role` key →
   `SUPABASE_SERVICE_KEY` (server-side only; never in a browser or a commit).
3. Storage → New bucket `bianca-studio`, **public** (Instagram must fetch the file).
   Only final renders are uploaded there; drafts stay private (`bianca-studio-private`).
4. SQL editor → run `supabase/migrations/001_init.sql`.

### 5. Meta / Instagram (the long one — budget 1–2 hours)
Requirements: @biancahome is an Instagram **Business** account (not Creator), linked to
a Facebook Page, both owned by the Bianca **Meta Business portfolio**.

1. Instagram app → Settings → Account type → confirm **Business**.
2. https://business.facebook.com → Settings → Accounts → Instagram accounts → confirm
   @biancahome is connected; Pages → confirm the Bianca Home Page; link them.
3. https://developers.facebook.com → My Apps → Create app → type **Business** →
   name `Bianca Studio` → attach to the Bianca business portfolio.
4. Add product **Instagram** (API setup with Facebook Login for Business).
5. Business settings → Users → **System users** → add `bianca-studio-bot` (Admin).
   Assign assets: the Bianca Home Page and @biancahome (full control), and the app.
6. Generate a token for the system user with permissions:
   `instagram_basic`, `instagram_content_publish` (shown as
   `instagram_business_content_publish` in newer app dashboards), `pages_show_list`,
   `pages_read_engagement`, `business_management`. Expiry: **never**.
   Copy → `META_ACCESS_TOKEN`.
7. Find the IG user id:
   `curl "https://graph.facebook.com/v21.0/me/accounts?fields=instagram_business_account&access_token=$META_ACCESS_TOKEN"`
   → `instagram_business_account.id` → `IG_USER_ID`.
8. Because the app is only used on Bianca's own assets by people with roles on the app,
   standard access is normally enough; App Review is only needed to post for other
   businesses. If Meta asks for review anyway, use the screencast flow in their docs.

Instagram limits that the pipeline enforces (tools/qc_technical.py):
MP4/MOV, H.264 or HEVC, AAC ≤48 kHz, 23–60 fps, 9:16, 5–90 s for the Reels tab,
≤100 MB via API, moov atom at the front. API posts are rate-limited per 24 h; check
`GET /{IG_USER_ID}/content_publishing_limit` (far above what we need).

### 6. Music
Instagram's in-app trending audio **cannot** be attached through the API. Options:
- **Meta Sound Collection** (free, cleared for FB/IG): download tracks into `assets/music/`.
- **Epidemic Sound / Artlist business plan** if you want more choice. Personal/creator plans
  do not cover brand accounts.
- Or post via API without music, then add trending audio by hand in the app (loses automation).
Never use commercial songs without a licence — brand accounts get muted or taken down.

### 7. ElevenLabs (only if using voice-over)
1. https://elevenlabs.io → Creator plan.
2. Voice Library or Voice Design → pick/design one Indian-English brand voice. Do **not**
   clone a real person's voice without their written consent.
3. Copy API key → `ELEVENLABS_API_KEY`, voice id → `ELEVENLABS_VOICE_ID`.

### 8. GitHub (done)
Repo: `virangdalal-design/social-media-beautiful-home-decor`. Add the same env values as
GitHub Actions secrets only when Phase 2 automation runs in CI.

---

## C. What I need from you (send in one go)
1. The `.env` values above (paste them into `config/.env` yourself on your machine, or
   into the Claude Code environment secrets — **never in chat or in a commit**).
2. Bianca brand kit: logo files (SVG/PNG, light + dark), brand fonts, brand colours (hex),
   end-card wording, Instagram handle(s) to tag.
3. The first product, filled in per docs/07-PRODUCT-INTAKE.md (photos + facts).
4. Music choice (Meta Sound Collection vs paid library).
5. Nautica: is AI-generated imagery of Nautica products allowed under the licence, and
   does it need licensor approval? Until confirmed, first videos use Bianca-brand products.

---

## D. Phase 0 exit check
- [ ] `python -m bianca_studio.cli doctor` all green.
- [ ] `python -m bianca_studio.cli check-video <any test mp4>` passes the spec checks.
- [ ] One test Reel published to a **test** Instagram Business account (or published to
      @biancahome then archived) to prove the Meta token + public URL path works.
- [ ] Brand kit in `assets/brand/`.
- [ ] Human says "gate passed".

---

## E. Track B (later) — extra accounts for the four presenters
| Service | What for | Cost |
|---|---|---|
| Higgsfield (Basic+ plan + API credits) | Soul ID: locked face for each presenter | ~$30–50/month + credits |
| ElevenLabs Creator/Pro | One designed voice per presenter | $22–99/month |
| Budget per presenter lock (reference pack + Soul ID + voice) | | ₹1,000–2,000 ($12–24) |
