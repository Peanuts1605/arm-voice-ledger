# Arm Voice Ledger Demo Evidence

## Decision

**READY_FOR_PUBLIC_VIDEO_UPLOAD.** The local evidence walkthrough is generated
from the real, automated browser proof rather than from presentation mockups.
It is intentionally a short silent walkthrough with captions; it is ready to
be paired with a brief narrated contest demo later without changing the app.

## Artifact

- Video: `demo/arm-voice-ledger-evidence-walkthrough.mp4`
- Format: H.264, 1920 x 1080, 30 fps, 13.37 seconds, 308,302 bytes
- SHA-256: `9375d8dc91a2db561ac7a6b481018d978f4b47a31b2f6f3d55df042775e0ff73`
- State: local proof asset; not yet uploaded to a public video host.

## What A Judge Sees

1. **Choose a short local voice note**
2. **Turn timestamps into evidence**
3. **Replay the moment behind each decision**

The three scenes are captured by `scripts/render-forge.mjs` after the actual
desktop browser flow has loaded the synthetic WAV, produced timestamped words,
created a ledger row, replayed its linked moment, and exported local JSON.

## Reproduce

```bash
PORT=18788 ./scripts/run-forge.sh
ARM_VOICE_LEDGER_URL=http://127.0.0.1:18788 npm run test:browser
./scripts/make-evidence-walkthrough.sh
```

The test writes the source PNGs under `demo/evidence/`; the walkthrough script
uses the project virtual environment's private FFmpeg binary. Both generated
video and temporary evidence stills are deliberately ignored by Git.

## Verification Snapshot

- Browser proof: desktop and mobile PASS
- Timestamped words: 16 on both viewports
- Ledger rows: 1 on both viewports
- Source URL: local browser `blob:` URL on both viewports
- Row replay: starts playing at 0.62 seconds on both viewports
- Cleared selection: hidden; create action disabled after row creation
- Browser console errors: 0
- Python suite: 7 passing
- Production dependency audit: 0 vulnerabilities

## Limits

This is a reproducible visual evidence asset, not a narrated final contest
video. The Arm challenge permits a public video up to three minutes, so the
smallest next presentation step is to upload this proof or add a short narrated
companion cut; neither requires a new product feature.
