# 02 — Architecture

## Flow (LangGraph)
```
product_brief → strategist → (interrupt: human picks angles; default all 4)
  → director (per angle) → shot_list
  → per shot (parallel, max 4):
       4 keyframes (Nano Banana Pro / GPT Image) → keyframe_qc (Gemini) → human picks → retry ≤2
       → video on top `best_of` final-tier models → shot_qc (Gemini + ffprobe) → retry ≤3
  → upscale (Topaz) → voice/music → assemble (Remotion + FFmpeg) → final_qc
  → (interrupt: human approval) → approved → publish (Instagram Graph API)
                                 | rejected{comment} → classify → director|producer
```
Interrupts use LangGraph checkpointing (Postgres saver on Supabase); a job can wait
days for approval and resume.

## State (src/bianca_studio/state.py)
job_id, product_brief, angles[], selected_angle_ids[], shot_lists{angle_id}, shots{shot_id:
keyframe_url, keyframe_attempts, video_url, video_attempts, model, qc_reports[], cost},
voice_url, assembled_url, final_qc, approval{status, comment}, total_cost, errors[]

## Services
| Concern | Service | Wrapper |
|---|---|---|
| Keyframes / product placement | Nano Banana Pro, GPT Image via fal | tools/images.py |
| Video | Seedance 2.5, Kling O3, Veo 3.1 via fal (Kling 4.0 when API live) | tools/video.py |
| Upscale | Topaz via fal | tools/video.py |
| Identity (Track B) | Higgsfield Soul ID | docs/characters/presenters.yaml |
| Publishing | Instagram Graph API | tools/instagram.py |
| Voice | ElevenLabs | tools/voice.py |
| QC vision | Gemini (video + image input) | tools/qc_gemini.py |
| QC technical | ffprobe / ffmpeg | tools/qc_technical.py |
| Assembly | Remotion CLI + FFmpeg | tools/assemble.py |
| Storage / DB | Supabase | tools/storage.py, tools/db.py |

## Data model
See supabase/migrations/001_init.sql: products, jobs, angles, shots, generations (every
paid call), qc_reports, approvals, benchmark_runs, benchmark_ratings.

## Model router
config/models.yaml selects by `purpose` (final | human_motion | product_macro | cinematic |
motion_control); `draft` exists for motion exploration only. Phase 3 adds learned scores per (product_category, shot_type, model).

## Approval surface
Phase 2: Next.js page on Railway reading Supabase. Later: WhatsApp/Telegram bot with the
same actions: approve, reject(comment), regenerate(shot_id, note).

## Reference-video input (Phase 3)
Optional `reference_video_url` on the brief. Strategist extracts hook/structure/pacing
(Gemini watches it). Director mirrors beat structure. Producer may pass the video as a
motion reference (Kling 3.0 Motion Control, Seedance omni-reference @Video).
Never copy audio, on-screen text, or a recognizable person from the reference.
