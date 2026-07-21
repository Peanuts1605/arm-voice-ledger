# Arm Voice Ledger Reproducible Smoke Proof Receipt

- Receipt ID: `ARM-VOICE-LEDGER-REPRODUCIBLE-SMOKE-PROOF-2026-07-20`
- Agent: ORION_L
- Date: 2026-07-20
- Status: complete
- Decision: `REPRODUCIBLE_SMOKE_PROOF_PASSED`

## Artifact

- Decision note: `docs/ARM_VOICE_LEDGER_REPRODUCIBLE_SMOKE_PROOF_2026-07-20.md`
- Public-safe fixture generator: `scripts/make-synthetic-fixture.sh`
- JSON receipt producer: `scripts/forge_smoke.py --receipt <path>`
- Receipt regression test: `tests/test_forge_smoke.py`
- Public source: https://github.com/Peanuts1605/arm-voice-ledger

## Verification

- Generated a local 16 kHz mono synthetic WAV with macOS `say` and `afconvert`.
- Offline local smoke replay: 16 timestamped words; 140 ms; MLX Whisper tiny;
  `offlineModelCache=true`; `audioPersisted=false`.
- `python3 -m unittest discover -s tests -v`: 8 passed.
- `ARM_VOICE_LEDGER_URL=http://127.0.0.1:18790 npm run test:browser`: passed
  desktop and mobile interaction flows with no console errors.
- `npm audit --omit=dev --audit-level=high`: 0 vulnerabilities.
- Local runner: stopped after verification.

## Scope

- The generated WAV and JSON run receipt are local and Git-ignored.
- No raw audio, transcript, model cache, credential, environment file, or
  account data is included in this proof package.
- This proof records a warm local measurement; it does not promise identical
  performance on other hardware.

## Shared Proof Reconciliation

- Drive delivery folder: `TMN_NAUMIO_HQ/06_DELIVERY/ARM-VOICE-LEDGER-REPRODUCIBLE-SMOKE-PROOF-2026-07-20`
- Initial Drive mirror run: `20260721T001521110Z`
- Initial receipt mirror SHA-256: `ec2ba1e2ee32abba0a22bfa5417a5fec6caf7af0ffa9b83aba1d227a15e88f66`
- Notion pointer: https://app.notion.com/p/3a4b143d291781f081a4dab108b59811
- Reconciled receipt mirror: `ARM_VOICE_LEDGER_REPRODUCIBLE_SMOKE_PROOF_RECEIPT_2026-07-20.reconciled-20260721T001609574Z.md`
  (SHA-256 `e3ac5bdf0003843ddfc2790e27a2b43cee99a20b34ec01d320f0b9854b3efcc1`)
