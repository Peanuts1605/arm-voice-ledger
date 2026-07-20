# Arm Voice Ledger Public Package Decision

- Date: 2026-07-20
- Owner: ORION_L
- Contest: Arm Create: AI Optimization Challenge
- Selected track: Mobile AI
- Decision: `PUBLIC_PACKAGE_READY`

## Product decision

Enter Arm Voice Ledger as a small on-device evidence workflow, not as a generic
transcription app. The useful differentiator is that a human-owned decision
remains attached to the exact local audio moment that supports it.

## What changed

- Created the public MIT repository:
  <https://github.com/Peanuts1605/arm-voice-ledger>
- Added a pinned Apple-silicon bootstrap path for MLX 0.32.0, mlx-whisper 0.4.3,
  and imageio-ffmpeg 0.6.0.
- Made the smoke route support explicit first-run online cache warm and normal
  offline replay modes.
- Moved the browser evidence gate to a project-local Playwright dependency.
- Fixed a rendered mobile/desktop state defect where a cleared selection strip
  could remain visible; the render gate now protects that state.
- Made timestamp actions replay local audio from the selected evidence point.

## Evidence

| Gate | Result |
| --- | --- |
| Public source | `Peanuts1605/arm-voice-ledger` is public at commit `539a72a8a953e8f008260e036b854d2f39de61f2` |
| License | GitHub API reports `MIT` |
| Fresh Arm64 setup | Apple M4, 32 GiB unified memory; pinned environment installed cleanly |
| First-run cache warm | 16 timestamped words in 339 ms; no retained audio |
| Offline replay | 16 timestamped words in 2.359 s; `offlineModelCache=true`; no retained audio |
| Unit tests | 7 passed |
| Browser gate | desktop and mobile passed selection, row creation, replay, export, cleared state, and zero console errors |
| Dependency audit | `npm audit --omit=dev --audit-level=high`: 0 vulnerabilities |

## Current tool check

The MLX Whisper official example supports `word_timestamps=True`, which is the
specific technical capability this product turns into replayable evidence.
The current route remains the smallest useful one: local MLX Whisper with
explicit offline cache proof. No capability change required a different
product path.

## Honest status

The Arm contest is open through 2026-08-14 4:00 PM PDT. Its rules require a
public MIT or Apache-2.0 repository, detailed project description, Arm64
setup instructions, and working testing access; the public package now covers
those technical requirements. A video is optional but recommended.

The live Devpost account is authenticated as `Peanuts1605` but is not yet
registered for the Arm challenge. The official rules also require an Arm
Developer Program account. No registration, declaration, or final submission
was made in this pass.

## Next action

Create the Devpost entry draft, select Mobile AI, and add the repository plus
the prepared description. Keep final terms and eligibility attestations for
the entrant. Add a concise live demo video before final submission if the
local capture route is ready.

## Transfer rule

For an Arm contest, a measured local proof is not enough. Package the exact
environment, verify the user-visible interaction on both form factors, and
make the public repository independently runnable before writing the pitch.
