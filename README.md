# Bianca Studio — AI Influencer Video Pipeline

Product photos + description in → four creative angles → shot lists → keyframes →
AI-generated video on top-tier models → upscale + finish → auto QC → human approval →
published on @biancahome.

**Now (Track A):** brand videos for Bianca Home's Instagram — no influencer.
**Later (Track B):** four AI presenters (informative, aspirational, comic, luxury).

## Start here
1. `docs/00-SETUP.md` — every account, purchase and key, in order.
2. `make setup` → fill `config/.env` → `make doctor` until green.
3. `docs/07-PRODUCT-INTAKE.md` — what to send for the first product.

Built for Bianca Home (bedding, bath, dining; Nautica license). Quality bar: content
you would actually post. If it is not that, it does not ship.

## How this repo is meant to be used

This is a **Claude Code project**. Open it in Claude Code and work phase by phase:

```
claude
> Read CLAUDE.md and docs/00-SETUP.md. We are starting Phase 0. Tell me what you need from me.
```

Claude Code reads `CLAUDE.md` first, then the docs, then builds against the specs in
`agents/`, `schemas/` and `config/`. Every phase has an exit gate. Do not skip gates.

## Layout

```
CLAUDE.md                 Operating instructions for Claude Code (read first)
docs/00-SETUP.md          Accounts, purchases, keys, Instagram connection
docs/01-PLAN.md           Phases, deliverables, gates, budget
docs/02-ARCHITECTURE.md   LangGraph flow, state, data model, services
docs/03-QUALITY-BAR.md    What "really good" means, as checkable rules
docs/04-SKILLS-AND-REPOS.md  What to install, what to verify before trusting
docs/07-PRODUCT-INTAKE.md    What to send per product
docs/characters/          Track B presenters (Meera, Kabir, Rohan, Anaya) + bible template
docs/06-BENCHMARK.md      10-shot model test + blind rating sheet
agents/*.md               System prompts for the four agents
schemas/*.json            JSON contracts between agents
config/models.yaml        Model router table (edit this, never hardcode models)
config/.env.example       Keys needed
src/bianca_studio/        Python skeleton (LangGraph graph, nodes, tool wrappers)
supabase/migrations/      Database schema
remotion/                 Brand templates (captions, end card, lower thirds)
assets/                   Product photos, brand kit, music, presenter packs, reference videos
tests/                    pytest (config, schemas, delivery encode/QC, Instagram client)
archive/                  Earlier attempts, reference only
```

## CLI
```
python -m bianca_studio.cli doctor            # accounts + keys + tools
python -m bianca_studio.cli encode in.mov reel.mp4   # Instagram delivery encode + check
python -m bianca_studio.cli check-video reel.mp4
python -m bianca_studio.cli publish reel.mp4 --caption-file caption.txt   # dry run
python -m bianca_studio.cli publish reel.mp4 --caption-file caption.txt --yes  # after approval
```

## Phases (summary)

| Phase | Outcome | Gate |
|---|---|---|
| 0 Connect | All accounts + keys, brand kit, test publish | `doctor` green + test Reel published |
| 1 One perfect video | One 15s brand video made semi-manually | You would post it as-is |
| 2 Pipeline | Four agents + QC loop + approval page | 3 videos pass QC and approval without manual fixes |
| 3 Scale | Benchmark, router, scheduling | Cost/quality per model known; 4 angles per product |

See `docs/01-PLAN.md` for the full version.
