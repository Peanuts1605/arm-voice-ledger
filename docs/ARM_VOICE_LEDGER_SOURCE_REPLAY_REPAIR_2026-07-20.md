# Arm Voice Ledger: Source Replay Repair

- Date: 2026-07-20
- Owner: ORION_L
- Contest route: Arm Create: AI Optimization Challenge
- Validation surface: Forge, Apple M2 Pro / Arm64 / 16 GiB unified memory
- Decision: `SOURCE_REPLAY_CONTRADICTION_REPAIRED`

## Finding

The product said a decision could point back to the exact moment that earned
it, but the first vertical proof displayed only textual timestamps. A person
could see a time such as `0:00.6`, yet could not replay the selected source
from the app. That made the strongest product claim stronger than its
interaction.

## Repair

The listening desk now keeps a browser-tab-only object URL for the selected
WAV and exposes it in a native local audio player. The server route remains
unchanged: it receives the WAV only for the request, writes a temporary file
for local MLX Whisper, then removes that server-side copy before responding.

- Selecting a transcript word cues the local player to that word's start time.
- Each editable ledger row has a `Cue m:ss.s` control that cues the player to
  the evidence range's start.
- Replacing or clearing the selected source revokes the prior browser object
  URL.

The browser player is intentionally a local review surface, not a persistence
or sharing feature.

## Forge Reproduction

The same synthetic public-safe WAV used for the vertical proof was replayed on
Forge with the cached MLX Whisper model forced offline.

| Check | Observed result |
| --- | --- |
| Forge unit suite | 7 passed |
| Local unit suite | 7 passed |
| Synthetic transcription | 16 timestamped words |
| Model mode | cached `mlx-community/whisper-tiny`, offline cache true |
| Synthetic API run | 762 ms, 438,321,152-byte peak RSS |
| Desktop browser replay | one ledger row, local source URL, transcript cue 2.3s, ledger cue 0.62s |
| Mobile browser replay | one ledger row, local source URL, transcript cue 2.3s, ledger cue 0.62s |
| Browser console | no errors |

The browser checks did not merely inspect the player markup. They selected a
nonzero transcript moment, created a ledger row from it, clicked both cue
paths, and read the local player's resulting playback position.

## Rendered Evidence

- Desktop: `demo/forge-listening-desk-desktop.png`
- Mobile: `demo/forge-listening-desk-mobile.png`
- Browser record: `demo/render-check.json`

The player, timestamped transcript, and ledger cue control are visible on both
screens. The source fixture and exported local JSON remain local-only and are
not part of the shared package.

## Scope and Limits

- Only synthetic, public-safe audio was used.
- This repair does not claim noisy-phone, long-recording, multilingual, or
  human-audio performance.
- No public repository, contest registration, public demo, or submission was
  created by this repair.
- The server and local SSH tunnel were stopped after verification.

## Next Product Gate

Give the revised product claim and Forge replay evidence to an independent
reviewer. The useful question is now concrete: does returning to the exact
audio moment make the editable decision ledger materially more trustworthy
than a generic transcript summary?

## Transfer Rule

When a product claims evidence is traceable, test the return path as a real
user action. Rendering a timestamp is not proof that a person can inspect the
source it represents.
