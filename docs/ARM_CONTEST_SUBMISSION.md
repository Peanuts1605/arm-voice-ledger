# Arm Voice Ledger - Arm Create Submission Draft

## Track

**Mobile AI**

## One-line pitch

Arm Voice Ledger turns a short voice note into a small, editable decision
ledger where every saved item can replay the exact local audio moment that
earned it.

## Project overview

Voice notes are wonderfully quick to create and notoriously hard to recover.
Most transcription tools flatten them into a summary that is difficult to
trust: the useful decision and the evidence for it get separated.

Arm Voice Ledger is a deliberately narrow local listening desk for Apple
silicon. A person chooses a short WAV, MLX Whisper returns word-level
timestamps, and the person selects only the ranges worth preserving as
decisions, next actions, or questions. Each row remains editable and its
**Replay** control returns to the exact local source moment.

This is not a meeting summarizer. It is a small evidence loop: source ->
timestamped moment -> human-owned decision -> replayable proof.

## Why it belongs in Mobile AI

The project uses MLX Whisper on Arm64 Apple silicon rather than sending the
selected audio to an application server. The small `whisper-tiny` model is
chosen for a bounded, local workflow. After an explicit first-run cache warm,
the default runner forces both Hugging Face and Transformers into offline mode.

That produces a practical Mobile AI optimization story:

- local Arm64 inference for a short voice-note workflow;
- word-level timestamps turned into reusable interaction, not just displayed;
- no user account, no transcription database, and no application-server audio
  path;
- a reproducible cache-warm then offline-replay setup for another Apple-silicon
  developer.

## What it does

1. A person selects a short WAV (up to 8 MB).
2. The local server uses MLX Whisper and removes its temporary request file
   before returning the result.
3. Timestamped words appear as selectable evidence.
4. A selected range becomes an editable Decision, Next action, or Question.
5. The saved row replays the local browser-tab source from its evidence point.
6. The person can explicitly export the ledger as local JSON.

## Measured proof

All measurements below use a local synthetic/public-safe fixture. No personal,
customer, or client audio was used. The fixture is intentionally not committed
to the public repository.

| Surface | Result |
| --- | --- |
| Forge vertical proof | Apple M2 Pro / 16 GiB unified memory; 16 timestamped words; cached offline model; source and ledger replay verified |
| Fresh current setup | Apple M4 / 32 GiB unified memory; `mlx==0.32.0`, `mlx-whisper==0.4.3`, `imageio-ffmpeg==0.6.0` installed from the pinned requirements |
| First-run cache warm | 16 timestamped words in 339 ms; `offlineModelCache=false`; `audioPersisted=false` |
| Offline smoke replay | 16 timestamped words in 2.359 s; `offlineModelCache=true`; `audioPersisted=false` |
| Desktop and mobile browser gate | 16 words, one editable ledger row, local source URL, replay started from both evidence paths, JSON export, no console errors |

Current visual evidence:

- [Desktop listening desk](../demo/forge-listening-desk-desktop.png)
- [Mobile listening desk](../demo/forge-listening-desk-mobile.png)

## How to run and validate

Run the pinned setup and first local cache warm from the [README](../README.md).
Then use the explicit smoke command with any short public-safe WAV:

```bash
VOICE_LEDGER_URL=http://127.0.0.1:8788 \
  ./.venv/bin/python scripts/forge_smoke.py /path/to/public-safe-fixture.wav
```

The server binds to `127.0.0.1` only. The health endpoint reports the selected
model, whether the cache is offline, and that request audio is not retained.
The unit suite validates input guards, source-name safety, private ffmpeg setup,
timestamp extraction, offline-mode behavior, and local source replay support.
For the optional desktop/mobile browser interaction gate, run `npm install`,
start the local server, and use `npm run test:browser` as documented in the
README.

## Why this should win

The project makes on-device model output useful rather than merely local. A
word timestamp is not treated as decoration: it is the bridge between a human
decision and the audio that supports it. The result is a clear, small workflow
that shows Arm64 local inference, a replayable trust mechanism, and a setup
another developer can reproduce.

## Honest limits

- WAV only, up to 8 MB.
- The proof uses a short English synthetic fixture.
- No claim is made about noisy-phone audio, multilingual quality, long
  recordings, battery impact, or a mobile-phone build.
- The browser-tab source exists only for local replay during the current
  session; server-side request audio is removed after transcription.
