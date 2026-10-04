# 06 — Model benchmark

Purpose: decide routing from your own data, not from YouTube.

## Fixed test set (10 shots, same keyframe for every model)
1. Printed bedsheet macro, slow push-in, window light
2. Towel texture close-up, hand runs across pile
3. Bed being made, wide, Rohan in frame, product print visible
4. Rohan holding folded sheet set to camera, speaking (lip-sync)
5. Rohan walking into bedroom, product on bed, handheld settle
6. Dining runner on table, pan across place settings
7. Nautica logo embroidery close-up (fidelity stress test)
8. Night scene, warm lamp, duvet turndown
9. Two-person scene (Rohan + second character) — consistency stress
10. Product-only pack shot rotating 30°

## Candidates (edit as models change)
Seedance 2.5 (omni-reference) · Kling O3 Pro · Kling 3.0 Pro · Veo 3.1 · Gemini Omni Flash ·
Kling 4.0 (when API live). Keyframes: Nano Banana Pro · GPT Image 2.
Run the benchmark during Phase 1 on shots 1, 2, 6, 7, 8, 10 (no presenter needed); the
presenter shots (3, 4, 5, 9) run in Track B.

## Low-cost comparison
Run the same shots through `comparison:` in config/models.yaml (free / cheap models) in the
same blind rating. Purpose: know exactly what the extra spend buys, and catch a cheap model
that has caught up. A comparison model is promoted into `video.tiers` only by beating a
final-tier model on quality in the blind rating, never on price.

## Text-agent comparison
Same product brief → Strategist (4 angles + captions) and Director (shot list) run on Claude
(llm: in config/models.yaml) and on each `comparison.llm` model (GPT-6 Astra, DeepSeek V4 Pro,
DeepSeek Flash). Outputs are stripped of model names, shuffled, and rated blind on: hook
specificity, brand voice, product accuracy (no invented claims), caption quality, and whether the
shot list is producible. Record cost per run. Promote only on a quality win.

## Procedure
1. Generate each shot on each model, same keyframe, same prompt skeleton, 1080p where supported.
2. Strip model names; shuffle. Three raters score blind on the 9 metrics (docs/03).
3. Record cost, generation time, retries needed to reach a usable take.
4. Write results to `benchmark_runs` / `benchmark_ratings`. Compute quality per $.
5. Update config/models.yaml routing. Re-run on every major model release.
Budget: ~₹5,000–8,000 per full run.
