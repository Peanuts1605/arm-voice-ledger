# Arm Voice Ledger Source Replay Repair Receipt

- Receipt ID: `ARM-VOICE-LEDGER-SOURCE-REPLAY-REPAIR-2026-07-20`
- Agent: `ORION_L`
- Date: `2026-07-20 America/New_York`
- Status: `LOCAL_VALIDATION_COMPLETE_SHARED_RECONCILIATION_PENDING`
- Decision: `SOURCE_REPLAY_CONTRADICTION_REPAIRED`

## Artifact

- [Source replay repair](../docs/ARM_VOICE_LEDGER_SOURCE_REPLAY_REPAIR_2026-07-20.md)

## Verification

- Local: `python3 -m unittest discover -s tests -v` -> `7 passed`.
- Local syntax: `python3 -m py_compile server.py`, `node --check web/app.js`,
  and `node --check scripts/render-forge.mjs` -> passed.
- Forge: `python -m unittest discover -s tests -v` -> `7 passed`.
- Forge synthetic MLX request -> 16 words, cached offline model true, audio
  persisted false, 762 ms, 438,321,152-byte peak RSS.
- Playwright replay -> desktop and mobile each created one ledger row, used a
  local browser `blob:` source, and verified transcript/ledger cue positions
  above zero with no console errors.
- The latest desktop and mobile screenshots were visually inspected.
- The Forge runner and local SSH tunnel were stopped after verification.

## Scope

- The fixture was synthetic and public-safe.
- No source WAV, exported local JSON, model cache, credential, environment
  file, or raw transcript is included in the shared package.
- No public repository, contest registration, public demo, or final submission
  was performed.

## Shared Proof Reconciliation

- Drive mirror: `TMN_NAUMIO_HQ/06_DELIVERY/ARM-VOICE-LEDGER-SOURCE-REPLAY-REPAIR-2026-07-20/`
- Notion pointer: https://app.notion.com/p/3a3b143d29178147a472f3a3a8e6514b
- Reconciled receipt mirror: helper run `20260720T230110609Z` hash-verified a
  copy containing the Drive and Notion references. This final local receipt is
  mirrored again after this reconciliation note.

## Next Action

Prepare the repaired local proof for independent product-claim review before
promoting it to a public contest repository.
