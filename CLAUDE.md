# CLAUDE.md — Bianca Studio

You are building an AI video content pipeline for Bianca Home. Read this file fully
before doing anything. Then read docs/00-SETUP.md, docs/01-PLAN.md and docs/03-QUALITY-BAR.md.

## What we are building
A pipeline that turns real product photos + a product brief into short vertical videos
that are indistinguishable from a real shoot, with automatic QC and human approval,
published to **Bianca Home's own Instagram account**.

Two tracks:
- **Track A — Brand videos (NOW).** No influencer. Product-hero lifestyle films for
  @biancahome: real-looking rooms, light, fabric, hands, anonymous people at most.
- **Track B — Presenters (LATER).** Four AI presenters, one per angle (informative,
  aspirational, comic, luxury). Specs live in docs/characters/. Not started until
  Track A has passed its Phase 1 gate.

Four agents: Strategist → Director → Producer → QC. See docs/02-ARCHITECTURE.md.

## Non-negotiable rules
1. **Quality over automation, quality over cost.** Phase 1 is done by hand until one video
   is genuinely post-worthy. Do not build orchestration before that gate is passed.
   Final renders only ever use the `final` tier in config/models.yaml. Never downgrade a
   final shot to a cheaper model to save money; escalate to the human instead.
2. **Keyframe first, always.** Every video shot starts from an approved still generated
   with the real product photos as references. Never text-to-video.
3. **Models live in config/models.yaml.** Never hardcode a model name in Python.
   The router reads the table. New models (Kling 4.0 API, Veo successors) must be a
   config change plus a benchmark run (docs/06-BENCHMARK.md), nothing else.
4. **Agents talk in JSON.** Every handoff validates against schemas/*.json. If an
   agent output fails validation, retry the agent once with the error, then fail loud.
5. **Retry caps.** Producer ↔ QC loop max 3 iterations per shot, then escalate to human.
   Log cost on every generation call.
6. **Product fidelity is checked, not assumed.** QC compares every shot against the
   original product photos (print, colour, weave, logo position). When a presenter is on
   camera (Track B), also against that presenter's reference pack.
7. **Text, logo, end card and CTA come from Remotion**, never from the video model.
8. **No face-swapping onto real footage.** No real person's likeness, ever.
9. **Verify before trusting third-party repos.** Check license, last commit, stars,
   and read the code of anything that touches API keys. Record findings in
   docs/04-SKILLS-AND-REPOS.md.
10. **Ask when the brief is thin.** If product info is missing (see docs/07-PRODUCT-INTAKE.md),
    ask the human instead of guessing.
11. **Nothing is posted without explicit human approval** of the exact final file and caption.

## Stack
- Orchestration: LangGraph (Python). Durable state, human-in-the-loop pause/resume.
- LLMs: Claude (Strategist, Director, Producer reasoning), Gemini (video QC — watches video).
- Generation gateway: fal.ai (one key → Seedance, Kling, Veo, Nano Banana, upscalers).
  Direct provider accounts only where a model is not on fal yet.
- Stills: Nano Banana Pro / GPT Image (keyframes with product references).
- Video: Seedance 2.5 (primary, omni-reference), Kling O3 / Kling 3.0 Pro, Veo 3.1.
  Kling 4.0 added when its API is live. Router + benchmark decide, not opinions.
- Finishing: Topaz upscale to 4K master → grade → Remotion (text, end card) → FFmpeg.
- Voice (optional VO): ElevenLabs. Music: licensed library only (docs/00-SETUP.md).
- Storage/DB: Supabase (Postgres + Storage; public URL needed for Instagram upload).
- Publishing: Instagram Graph API (Content Publishing) on @biancahome.
- Identity (Track B only): Higgsfield Soul ID.

## Conventions
- Python 3.11, `uv` for deps, `ruff` for lint, `pytest` for tests.
- One node per file in src/bianca_studio/nodes/. One wrapper per service in tools/.
- All generated media goes to Supabase Storage under `jobs/{job_id}/{stage}/`.
- Every generation call writes a row to `generations` with model, cost, duration, status.
- Secrets only via env (config/.env.example lists them). Never commit .env.
- `python -m bianca_studio.cli doctor` must pass before any paid run.

## How to work with Virang
- Short status updates. Lead with what's blocked or what needs his decision.
- When presenting creative output, present 2–3 options, not one.
- Costs in ₹ and $ both.
- Flag anything that touches the Nautica license or AI-disclosure rules.

## Phase gates (do not proceed without the human saying "gate passed")
- Phase 0 → 1: all accounts connected (`doctor` green), test Reel published privately/drafted.
- Phase 1 → 2: one 15s brand video Virang would post unedited.
- Phase 2 → 3: 3 consecutive products through the full pipeline with ≤1 human edit each.
- Track B starts only after Phase 1 gate; each presenter has its own lock gate (docs/characters/).

## Legacy
archive/ holds the earlier attempts (Rohan persona plan, simple Python pipeline). Reference
only — do not run archive/v1-python-pipeline/pipeline.py (text-to-video, hardcoded models).
