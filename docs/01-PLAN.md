# 01 — Plan

## Goal
Post-quality short vertical videos (9:16, 15–30 s) for Bianca Home products, published on
@biancahome, that look like a real high-end shoot. Human only approves, never fixes.
Quality is the constraint; cost is tracked, not optimised, until Phase 3.

## Track A — Brand videos (now)

### Phase 0 — Connect everything (Week 1)
1. Create accounts and keys per docs/00-SETUP.md. `cli doctor` all green.
2. Confirm every model id in config/models.yaml on fal; set `endpoints_verified: true`.
3. Brand kit into assets/brand/ (logo, fonts, colours, end-card wording).
4. Remotion: build `EndCard` and `Caption` templates from the brand kit.
5. Prove the publish path: upload a test MP4 to Supabase public bucket → publish to a test
   IG Business account (or publish + archive on @biancahome).
Deliverable: green doctor, brand templates, one successful API publish.
Gate: human says "gate passed".
Budget: ₹0–2,000 (subscriptions only).

### Phase 1 — One perfect video, by hand (Weeks 2–3)
Hero product: a printed bedsheet set (hardest fidelity case) unless Virang picks another.
1. Fill the brief (docs/07-PRODUCT-INTAKE.md → schemas/product_brief.json).
2. Run agents/strategist.md in Claude manually → 4 angles → Virang picks one.
3. Run agents/director.md manually → shot list (schemas/shot_list.json).
4. Per shot: 4 keyframe candidates (Nano Banana Pro / GPT Image, product photos as refs)
   → approve one → generate on the top 2 final-tier models for the shot's purpose
   → QC + human review → regenerate until right. Log every attempt and cost.
5. Upscale (Topaz) → grade → Remotion (text, end card) → FFmpeg delivery encode
   → `cli check-video`.
6. Iterate until Virang would post it unedited. Publish via `cli publish` after approval.
Deliverable: 1 posted video + a log of prompts/settings that worked (feeds agents/).
Gate: "I would post this." If 3 weeks pass without it, rethink models, not agents.
Budget: ₹15,000–20,000 ($170–230) in generations.

### Phase 2 — Automate (Weeks 4–6)
1. Supabase schema (supabase/migrations/001_init.sql) + storage buckets.
2. LangGraph graph: strategist → director → [per shot: keyframes → video ×best_of → qc]* →
   voice/music → upscale → assemble → final_qc → human_approval → publish.
   Interrupts at angle pick and approval.
3. Tool wrappers in src/bianca_studio/tools/ (fal, gemini, supabase, instagram, ffmpeg).
4. QC agent: structured score (docs/03-QUALITY-BAR.md) + ffprobe checks.
   Fail → feedback JSON to Producer. Max 3 retries per shot per model, then escalate.
5. Approval page (Next.js on Railway reading Supabase): preview, score, cost,
   Approve & schedule / Reject with comment / Regenerate shot N.
6. Rejection routing: comment classified → Director (concept) or Producer (execution).
Deliverable: `make video PRODUCT=bedsheet-aurora-king` → approval request arrives.
Gate: 3 consecutive products, ≤1 human edit each.

### Phase 3 — Scale and learn (Weeks 7+)
1. All 4 angles per product by default; parallel shot generation.
2. Model benchmark (docs/06-BENCHMARK.md) on every major release; router updated from it.
   Add Kling 4.0 when its API is live.
3. Reference-video input: Strategist extracts structure → Director mirrors beats.
4. Scheduling + insights: hold rate / saves / shares / link clicks written back so the
   Strategist weights future angles. Carousels and Stories cut-downs from the same assets.

## Track B — Four presenters (after Track A Phase 1 gate)
One presenter per angle; specs in docs/characters/.
| Angle | Presenter (working name) |
|---|---|
| Informative | Meera |
| Aspirational decor lifestyle | Kabir |
| Comic, viral, youth | Rohan |
| Luxury aesthetic | Anaya |
Per presenter: 10 candidate looks → pick → 20-still reference pack → Higgsfield Soul ID →
designed ElevenLabs voice → bible filled → gate (10 new stills, blind-rated same person
by 3 people; voice approved). Order: Kabir → Anaya → Meera → Rohan (hardest last).
Budget: ₹1,000–2,000 ($12–24) per presenter + Higgsfield plan.
Before any presenter posts: ASCI virtual-influencer disclosure on every post.

## Budget (rough — confirm against config/models.yaml and provider pages)
| Item | Est. |
|---|---|
| Final-tier clip, per generated second | $0.30–1.15 |
| Keyframe still (4K) | $0.15–0.20 |
| Topaz video upscale, per second | ~$0.10 |
| Gemini QC per video | $0.10–0.30 |
| Finished 15 s video, best-of-2, ~2 retries/shot | ₹3,500–7,000 ($40–80) |
| Product, 4 angles | ₹14,000–28,000 ($160–320) |

## Legal / brand checklist (before first public post)
- [x] Nautica licence: AI-generated product imagery confirmed OK by Virang (2026-10-03).
- [ ] Output licences allow commercial use (fal model terms, Seedance, Kling, Veo, Topaz,
      ElevenLabs).
- [ ] Music licensed for brand use on Instagram.
- [ ] Meta's AI-content label: apply "AI info" where Meta requires it for photorealistic AI video.
- [ ] No real person's likeness anywhere.
- [ ] Track B only: ASCI virtual-influencer disclosure.
