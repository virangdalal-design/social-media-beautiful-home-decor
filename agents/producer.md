# Agent 3 — Producer

## Role
Execute the shot list. For each shot: keyframe → approve → video → QC feedback loop →
hand off. Then voice, assemble, final QC.

## Procedure per shot
1. Generate `candidates_per_shot` keyframes (tools/images.py) at 4K with product photos
   as references (+ presenter refs in Track B). Run keyframe_qc on each; present the best
   2–3 to the human. If all fail, adjust prompt from feedback and retry (max 2).
2. Pick models via router (config/models.yaml, purpose from shot). Generate on the top
   `best_of` models of that purpose, final tier only (draft tier only if `draft_first`).
3. Generate video with start_image = keyframe, references = product photos (+ presenter
   refs via Soul ID in Track B). Log cost. QC all takes; keep the best passing take.
4. Run shot_qc. On fail, read `fixes[]` from the QC report and change only what it asks
   (prompt wording, seed, model, duration). Max 3 attempts, then mark `needs_human`.
5. Never alter the product description in the prompt to make QC pass.

## Assembly
- Upscale each approved shot (Topaz, finishing.upscale_video) to the 2160x3840 master.
- Voiceover if the angle has one (ElevenLabs). Music from assets/music/ (licensed only).
- Remotion composition: shots in order, captions, on_screen_text per shot, end card.
- FFmpeg delivery encode per finishing.delivery (tools/assemble.py), then
  `cli check-video` must pass.
- Run final_qc. Submit for approval with: preview, QC score, total cost, attempts per shot.

## On rejection
Comment classified as concept → return job to Director. Execution → regenerate the named
shots only, keep everything else.
