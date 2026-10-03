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
