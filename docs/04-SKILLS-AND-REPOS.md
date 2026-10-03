# 04 — Skills and repos to use (and verify first)

Status column: `unverified` until someone has read the code and checked license + last
commit. Claude Code: update this table as you verify. Never install an unverified skill
into an environment that holds API keys.

| Layer | Repo / skill | Use for | Status |
|---|---|---|---|
| Generation gateway | fal.ai official Python client (`fal-client` on PyPI) | All model calls in tools/images.py, tools/video.py | unverified |
| Identity + generation (Track B) | github.com/higgsfield-ai/skills (`higgsfield-soul-id`, `higgsfield-generate`) | Train Soul ID; call Nano Banana 2, Seedance 2.5, Kling 3.0 from Claude Code | unverified |
| Prompt craft | github.com/OSideMedia/higgsfield-ai-prompt-skill | Seedance 2.5 omni-reference prompting, acting system, character anchor block | unverified |
| Kling prompting | github.com/maciejdzierzek/kling-ai-prompt-generator | Kling 3.0 I2V / motion control / multi-shot prompts | unverified |
| Assembly | Remotion official agent skills (`npx skills add remotion`) | Captions, end card, titles as React templates | unverified |
| Assembly QA | github.com/haidrrrry/claude-remotion-skill | Renders, extracts frames, inspects, fixes before delivering | unverified |
| Voice + FFmpeg | github.com/digitalsamba/claude-code-video-toolkit | ElevenLabs, FFmpeg, Remotion patterns | unverified |
| Editing tools | github.com/relo-video/synthcut | Local FFmpeg/Whisper MCP tools (cuts, captions) | unverified |
| Directory | github.com/zhuyansen/awesome-claude-video-skills | 180 video skills, security-graded; check monthly | reference |
| Fallback API pack | github.com/brycefinnerty/claude-code-ai-ad-builder-kie-ai | KIE.ai multi-model access if Higgsfield API is limiting | unverified |

## Verified (2026-10-03)
| Repo | Verdict | Findings |
|---|---|---|
| github.com/DietrichGebert/ponytail @ tag v4.9.0 | **installed** (project-level, `.claude/settings.json`) | MIT; commits daily; Claude Code plugin = prompt rules + skills + Node hooks (SessionStart, SubagentStart, UserPromptSubmit). Hooks read only their own env vars, write small mode/flag files under ~/.claude, no network calls, no child processes (`vm` only sandboxes a user regex). Note: some guides say `dietrichayala/ponytail` — that repo does not exist; never install from it (typosquat risk). Affects how Claude Code writes code in this repo, not the video pipeline. |
| github.com/addyosmani/agent-skills @ 0.6.12 (sha f01f649) | **installed** (project-level, `.claude/settings.json`, inline marketplace pinned to the commit — the repo's own marketplace.json tracks main, so pinning its ref alone would not pin the plugin) | MIT; Addy Osmani; active (release 2026-10-02); ~2 MB. Plugin = 25 Markdown skills (spec-driven dev, TDD, planning, code review, security, performance, debugging, shipping…) + slash commands (/spec, /plan, /build, /test, /review, /code-simplify, /ship, /webperf). No hooks wired by default (hooks/ has no hooks.json; the optional sdd-cache hooks only send HEAD requests to URLs already being fetched). Pairs with Ponytail: agent-skills sets process (spec → test → review), Ponytail keeps the code minimal. |
| github.com/Graphify-Labs/graphify (PyPI `graphifyy` 0.9.74) | **reviewed, awaiting Virang's go-ahead** (install blocked by session safety rules; needs a human decision) | Apache-2.0 + MIT; very active (release 0.9.74 on 2026-10-02); ~27 MB, 92 Python modules. Builds a knowledge graph of the repo: code parsed locally with tree-sitter (no LLM, nothing leaves the machine). Docs/images/video get a semantic pass only via the assistant's own model or an explicit `--backend` key. Caution: it auto-detects `GOOGLE_API_KEY` (our Gemini key) for that pass — never pass `--backend gemini` on assets/, or it spends money and uploads media. Official only: forks like `sharkkyyy10/graphify-` and `aiminnovations/claude-graphify` are copies — do not install. Install (human-run): `uv tool install "graphifyy==0.9.74"` then `graphify claude install --project` (writes `.claude/skills/graphify/`), review that diff, commit. |
| github.com/diegosouzapw/OmniRoute | **not installed** | MIT, very active, but ~760 MB / ~12k source files — cannot be code-reviewed per rule 9, and it would hold every API key. Core features route consumer subscriptions (Claude Pro, ChatGPT etc.) as APIs and use "TLS stealth" to avoid blocks — against provider terms, risks bans of the accounts we depend on. It is an LLM text gateway; our cost and quality live in video models on fal, which it does not replace. Our own router (config/models.yaml) + the comparison lane already cover model choice. Revisit only as a local, LLM-only experiment with pay-as-you-go API keys. |

## Deliberately NOT used
- SadTalker / gTTS / SD-1.5 influencer kits — 2023 quality.
- FaceFusion or any face swap onto real footage — consent and platform risk.
- Sora — no reference images; product fidelity unworkable.
- Veo 3.1 for product macros — reported weak on fine print/logo detail. It stays in the
  router for `cinematic` room shots only; the benchmark decides if that changes. Gemini API
  preview endpoints were reported shutting 22 Oct 2026: call Veo via fal, and confirm the
  Gemini QC model id is a GA (non-preview) id.
- ComfyUI / Wan self-hosting — only if volume justifies GPU ops (Phase 3+).

## Verification checklist per repo
- [ ] License allows commercial use
- [ ] Commit in last 90 days
- [ ] Read every file that reads env vars or makes network calls
- [ ] Pin the commit hash you installed
