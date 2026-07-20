# Arm Voice Ledger: Forge Vertical Proof

- Date: 2026-07-20
- Owner: ORION_L
- Contest: Arm Create: AI Optimization Challenge
- Validation surface: Forge, Apple M2 Pro / Arm64 / 16 GiB unified memory
- Decision: `LOCAL_VERTICAL_PROOF_PASSED`

## Product truth

People leave decisions in voice notes because speaking is easy, then lose the
reasoning when a generic transcript separates the summary from the source.
Arm Voice Ledger keeps a short WAV on-device long enough to create an editable,
timestamp-linked decision row and then removes the source request file.

The proof is a focused listening desk, not a meeting assistant: source audio,
word-level moments, and a decision ledger are visible at once.

## What now works

1. A person selects a WAV in a browser running against the local Forge server.
2. The browser sends it only to `127.0.0.1`; the server writes a temporary WAV
   for MLX Whisper and removes it before returning a response.
3. Forge runs cached `mlx-community/whisper-tiny` through MLX Whisper with the
   Hugging Face and Transformers offline flags enabled.
4. The UI displays timestamped words. Selecting a word range produces an
   editable Decision, Next action, or Question row with its quote and time
   range retained.
5. The ledger exports an explicit local JSON file. Nothing creates an account,
   stores a transcript, or posts audio to an application server.

## Real measured proof

The synthetic public-safe Forge fixture was transcribed by the new local HTTP
route with the cached model forced offline:

| Check | Observed result |
| --- | --- |
| Model | `mlx-community/whisper-tiny` through MLX `0.32.0` / mlx-whisper `0.4.3` |
| Offline condition | `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1` |
| Words returned | 16 timestamped words |
| API run latency | 781 ms |
| Peak resident memory | 437,223,424 bytes |
| Audio retention response | `false` |
| Forge server health | local model ready, cached offline mode `true` |
| Browser desktop replay | 16 words, one ledger row, local JSON export, no console errors |
| Browser mobile replay | 16 words, one ledger row, local JSON export, no console errors |

The browser replay showed 1.53 seconds for the first UI request and 0.18
seconds for the following warm replay. Those are UI-route observations, not a
claim about long-recording speed or transcription accuracy.

## Repair that mattered

MLX Whisper expects a command named `ffmpeg`; imageio-ffmpeg's bundled binary
has a versioned filename. The server now makes a private `.tools/ffmpeg`
symlink to the already-installed decoder and adds only that project-local
directory to its process PATH. No system package or global PATH was changed.

## Rendered evidence

- Desktop: `demo/forge-listening-desk-desktop.png`
- Mobile: `demo/forge-listening-desk-mobile.png`
- Browser test record: `demo/render-check.json`

The screenshots show the actual post-transcription state: selected source,
timestamped evidence, one editable decision row, and the local JSON export
control. The synthetic WAV and generated JSON are intentionally local-only
test artifacts and are not shared.

## Verification

```text
Local:  python3 -m unittest discover -s tests -v  -> 6 passed
Forge:  python -m unittest discover -s tests -v   -> 6 passed
Forge:  scripts/forge_smoke.py                    -> 16 words, offline cache true, audio persisted false
Browser: scripts/render-forge.mjs                 -> desktop and mobile pass, no console errors
```

Forge's runner and the local SSH tunnel were stopped after the browser replay.

## What this does not claim

- No human/client audio, long recording, noisy-phone audio, or multilingual
  quality claim has been tested.
- No public repository, Arm Program registration, Devpost project, or contest
  submission has been created.
- This is proof of a local technical core and a usable decision workflow, not
  a production privacy certification.

## Next product move

Ask an independent reviewer to attack the claim that the timestamped row is
more useful than a generic summary. If that holds, promote this exact local
proof into a public MIT repository with the Forge reproduction route, then
capture a 60-to-90 second demo around one source-to-ledger moment.

## Transfer rule

For a hardware contest, the UI must make the constrained runtime visible in
the moment a user gets value. A benchmark in a README is weaker than a working
local flow that shows its offline state, measured result, and source evidence
together.
