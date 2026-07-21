# Arm Voice Ledger Contest Demo

- Date: 2026-07-21
- Owner: ORION_L
- Decision: `READY_FOR_PUBLIC_VIDEO_UPLOAD`

## Artifact

- Local video: `demo/arm-voice-ledger-contest-demo.mp4`
- Reproducible generator: `scripts/make-contest-demo.sh`
- Rendered format: H.264, 1920 x 1080, 30 fps, 24.4 seconds
- SHA-256: `40b67689b4be37d36d603c67b93f1f2bc532ebf628213be5f4bdffa2bae41f60`

## Judge Story

1. A voice note becomes a decision only when the listener can return to the
   exact source moment that earned it.
2. The real product flow shows local WAV intake, timestamped evidence, and an
   editable decision ledger with local replay.
3. The closing frame names the actual proof boundary: public MIT source and a
   reproducible local smoke run.

The video uses only three rendered states emitted by the browser test after it
loaded the synthetic fixture, produced timestamped words, saved an editable
ledger row, and exercised local replay. It adds no synthetic product screens,
no generated voiceover, and no unmeasured performance claims.

## Verification

- `./scripts/make-contest-demo.sh` completed successfully.
- `ffprobe` confirmed `24.400000` seconds and a 1,006,582-byte MP4.
- Visual review of the title, product-evidence, and closing frames confirmed
  readable copy, an unclipped proof chip, and no font-fallback glyphs.
- Product behavior was not changed.

## Next Action

Use this asset as the public contest walkthrough when the Arm submission is
opened. Uploading or publishing it is intentionally separate from this local
evidence pass.
