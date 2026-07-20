# Arm Voice Ledger Public Package Receipt

- Receipt ID: `ARM-VOICE-LEDGER-PUBLIC-PACKAGE-2026-07-20`
- Agent: `ORION_L`
- Date: `2026-07-20 America/New_York`
- Status: `VALID_PENDING_ENTRY_DRAFT`

## Artifact

- Decision: `docs/ARM_VOICE_LEDGER_PUBLIC_PACKAGE_DECISION_2026-07-20.md`
- Public source: <https://github.com/Peanuts1605/arm-voice-ledger>
- Public commit: `539a72a8a953e8f008260e036b854d2f39de61f2`
- Submission draft: `docs/ARM_CONTEST_SUBMISSION.md`

## Verification

- `python3 -m unittest discover -s tests -v`: 7 passed.
- Pinned fresh setup installed successfully on Apple M4 / Arm64 / 32 GiB.
- Online cache warm returned 16 timestamped words in 339 ms with
  `audioPersisted=false`.
- Offline replay returned 16 timestamped words in 2.359 s with
  `offlineModelCache=true` and `audioPersisted=false`.
- `npm run test:browser` passed desktop and mobile source selection,
  timestamped evidence, row creation, replay, JSON export, cleared selection
  state, and zero console errors.
- `npm audit --omit=dev --audit-level=high`: 0 vulnerabilities.
- GitHub repository visibility: `PUBLIC`; GitHub license endpoint: `MIT`.

## Current tool capability decision

- Official MLX Whisper documentation confirms word-level timestamps, the
  narrow capability used by the product.
- `mlx-whisper==0.4.3` and `mlx==0.32.0` are pinned and were exercised on the
  current Apple-silicon machine.
- Decision: `REVIEWED_NO_ROUTE_CHANGE`.

## Forge note

- Tailscale reached Forge at `100.123.192.22` during this pass.
- The current SSH key was not accepted, so no fresh Forge shell command was
  claimed. Existing Forge proof remains recorded separately; this pass added a
  fresh independent Apple M4 Arm64 replay.

## Decision and next action

`PUBLIC_PACKAGE_READY`. The only remaining entry work is Devpost registration
and draft creation, including the Arm Developer Program requirement. A demo
video remains recommended, not required by the official rules.

## Shared proof reconciliation

- Drive path: `TMN_NAUMIO_HQ/06_DELIVERY/ARM-VOICE-LEDGER-PUBLIC-PACKAGE-2026-07-20/`
- Notion pointer: <https://app.notion.com/p/3a3b143d2917815593e5ca76ecdc5fc3>
- Re-mirrored reconciled receipt: the helper preserves the prior receipt and
  writes a timestamped reconciled copy with matching SHA-256 recorded in its
  delivery manifest.
