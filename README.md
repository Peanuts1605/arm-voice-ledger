# Arm Voice Ledger

Arm Voice Ledger is a small local listening desk for voice notes that contain
decisions, questions, or next actions worth revisiting. It transcribes a short
WAV on-device, preserves word timestamps, lets a person select source moments
into editable ledger rows, and exports local JSON.

It is not a meeting summarizer. A ledger row keeps the quote and timestamp that
earned it, so a person can return to the source rather than trust a detached
summary.

## Product truth

Voice notes are easy to make and hard to recover later. Arm Voice Ledger turns
a local recording into an editable decision ledger without an application
server audio path.

## Apple-silicon setup

This first vertical proof targets an Apple-silicon Mac. It was measured on the
verified Forge lab:

- Apple M2 Pro / Arm64
- MLX `0.32.0`
- `mlx-whisper` `0.4.3`
- cached `mlx-community/whisper-tiny`

From a fresh clone, create the pinned virtual environment:

```bash
chmod +x scripts/bootstrap-forge.sh scripts/run-forge.sh
./scripts/bootstrap-forge.sh
```

For the first transcription only, permit MLX Whisper to cache its selected
model locally. Choose a short, non-sensitive WAV in the browser, complete one
transcription, then stop the server. For a command-line proof of that cache
warm, use the explicit online expectation:

```bash
HF_HUB_OFFLINE=0 TRANSFORMERS_OFFLINE=0 ./scripts/run-forge.sh
VOICE_LEDGER_URL=http://127.0.0.1:8788 ./.venv/bin/python scripts/forge_smoke.py --expect-online /path/to/public-safe-fixture.wav
```

Later runs default to the cached offline model:

```bash
./scripts/run-forge.sh
```

Open `http://127.0.0.1:8788`. The runtime exposes `GET /api/health` and sends
no selected audio to an application server. The server uses a temporary WAV and
removes it as soon as MLX Whisper returns. The selected WAV remains available
only in the current browser tab for source replay.

## Smoke test

With the server running, pass a short public-safe fixture explicitly:

```bash
./.venv/bin/python scripts/forge_smoke.py /path/to/public-safe-fixture.wav
```

If you choose a non-default port, set it once for the smoke command:

```bash
VOICE_LEDGER_URL=http://127.0.0.1:18788 ./.venv/bin/python scripts/forge_smoke.py /path/to/public-safe-fixture.wav
```

The smoke test checks that timestamped words return while the model cache is
forced offline and that audio retention is reported as false.

## Local tests

```bash
python3 -m unittest discover -s tests -v
```

## Boundaries of this proof

- WAV only, up to 8 MB.
- The included Forge run uses synthetic/public-safe audio.
- The repository does not include voice recordings. Use your own
  non-sensitive WAV for first-run and smoke checks.
- No quality, privacy, multilingual, or long-recording claim is made beyond
  the tested local cached-model path.
- The app creates no user account and writes no transcript or ledger to a
  server. Export is an explicit local download.

## License

MIT. See `LICENSE`.
