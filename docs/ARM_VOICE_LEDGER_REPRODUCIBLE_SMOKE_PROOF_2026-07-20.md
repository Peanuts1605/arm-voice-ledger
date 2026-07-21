# Arm Voice Ledger: Reproducible Local Smoke Proof

- Date: 2026-07-20
- Owner: ORION_L
- Contest: Arm Create: AI Optimization Challenge, Mobile AI track
- Decision: `REPRODUCIBLE_SMOKE_PROOF_PASSED`

## Purpose

The public repository deliberately excludes audio recordings. This small proof
upgrade lets another developer regenerate a public-safe local WAV on macOS and
capture the same useful evidence shape without receiving a fixture from us.

It does not change the product flow, model, or privacy claim. It makes the
existing local proof easier to audit.

## Reproduction

```bash
./scripts/make-synthetic-fixture.sh demo/synthetic-forge-fixture.wav
./scripts/run-forge.sh
VOICE_LEDGER_URL=http://127.0.0.1:8788 \
  ./.venv/bin/python scripts/forge_smoke.py \
  --receipt demo/arm-voice-ledger-run.json \
  demo/synthetic-forge-fixture.wav
```

The generated WAV and JSON receipt are ignored by Git. The receipt records the
host runtime, pinned dependency versions, model, elapsed time, peak resident
memory, timestamped-word count, offline-cache state, and audio-retention
result.

## Fresh Local Evidence

The generated fixture was exercised on the current Apple-silicon Mac with the
cached model forced offline:

| Check | Result |
| --- | --- |
| Runtime | `arm64`, macOS 26.5.2, Python 3.14.6 |
| Model | `mlx-community/whisper-tiny` |
| Dependencies | MLX 0.32.0; mlx-whisper 0.4.3; imageio-ffmpeg 0.6.0 |
| Fixture | synthetic macOS voice, 16 kHz mono WAV, 165,808 bytes |
| Timestamped words | 16 |
| Warm local replay | 140 ms |
| Model cache | offline (`true`) |
| Request audio retained | `false` |

The 140 ms figure is a warm local replay on this machine. It is recorded as
evidence, not a cross-device performance promise.

## Regression Gate

- `python3 -m unittest discover -s tests -v`: 8 passed.
- `ARM_VOICE_LEDGER_URL=http://127.0.0.1:18790 npm run test:browser`: passed.
- Browser gate: desktop and mobile each returned 16 words, created one ledger
  row, used browser-local source replay, exported JSON, cleared selection, and
  logged no console errors.
- `npm audit --omit=dev --audit-level=high`: 0 vulnerabilities.
- Local runner: stopped after verification.

## Product Lesson

For an optimization contest, a metric table is weaker than a command that
creates its own safe input and saves a structured evidence record. The proof
stays honest when it names the exact runtime and avoids pretending timing will
transfer unchanged to another Arm device.
