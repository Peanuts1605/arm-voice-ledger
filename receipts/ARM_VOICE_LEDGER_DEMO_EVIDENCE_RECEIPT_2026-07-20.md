# Arm Voice Ledger Demo Evidence Receipt

- Receipt ID: `ARM-VOICE-LEDGER-DEMO-EVIDENCE-2026-07-20`
- Agent: ORION_L
- Date: 2026-07-20
- Status: complete
- Decision: `READY_FOR_PUBLIC_VIDEO_UPLOAD`

## Artifact

- Evidence note: `docs/ARM_VOICE_LEDGER_DEMO_EVIDENCE_2026-07-20.md`
- Local walkthrough: `demo/arm-voice-ledger-evidence-walkthrough.mp4`
- Browser capture source: `scripts/render-forge.mjs`
- Walkthrough generator: `scripts/make-evidence-walkthrough.sh`
- Public source repository: `https://github.com/Peanuts1605/arm-voice-ledger`

## Verification

- H.264 MP4: 1920 x 1080, 30 fps, 13.366667 seconds, 308,302 bytes
- Video SHA-256: `9375d8dc91a2db561ac7a6b481018d978f4b47a31b2f6f3d55df042775e0ff73`
- `ARM_VOICE_LEDGER_URL=http://127.0.0.1:18788 npm run test:browser`: PASS
- Desktop/mobile: 16 timestamped words, one ledger row, local `blob:` audio,
  replay active at 0.62 seconds, cleared selection hidden, create action disabled
- `python3 -m unittest discover -s tests -v`: 7 passed
- `npm audit --omit=dev --audit-level=high`: 0 vulnerabilities
- Local runner: stopped after verification

## Shared Proof Reconciliation

- Drive delivery folder: `TMN_NAUMIO_HQ/06_DELIVERY/ARM-VOICE-LEDGER-DEMO-EVIDENCE-2026-07-20`
- Initial Drive mirror run: `20260720T235637143Z`
- Initial video mirror SHA-256: `9375d8dc91a2db561ac7a6b481018d978f4b47a31b2f6f3d55df042775e0ff73`
- Notion receipt: https://app.notion.com/p/3a3b143d291781e5ac7bec63215ba568
- Reconciled receipt mirror: `ARM_VOICE_LEDGER_DEMO_EVIDENCE_RECEIPT_2026-07-20.reconciled-20260720T235748590Z.md`
  (SHA-256 `9eb7048026ba7a010b03b37b3d45a3e854e80c9feb998394fd190bb8e24095e5`)

## Notes

The video is generated from real test states. It is not yet uploaded to a
public video host; the code and reproduction instructions are already public.
