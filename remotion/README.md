# Remotion brand templates (Phase 1 builds these)
Compositions to create:
- `Reel` — stitches shot clips, applies captions (word-synced from ElevenLabs timestamps),
  per-shot on_screen_text, and the EndCard. Props: shots[], captions, product, brand.
- `EndCard` — 2s: logo, product name, CTA. Variants: bianca_home, nautica, bianca_maison.
- `Caption` style: brand font, 2 lines max, safe area 1080x1920 (keep 220px clear at bottom).
Brand inputs: assets/brand/ (logo, fonts, colours). Music: assets/music/ (licensed only).
Install: `npx skills add remotion` (verify first, see docs/04). Render via CLI from tools/assemble.py.
