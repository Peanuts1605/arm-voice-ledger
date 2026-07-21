#!/usr/bin/env bash
set -euo pipefail

# Public-safe, local-only smoke input. The audio file remains ignored by Git.
output_path="${1:-demo/synthetic-forge-fixture.wav}"
output_directory="$(dirname "$output_path")"
temporary_aiff="$(mktemp "${TMPDIR:-/tmp}/arm-voice-ledger-fixture.XXXXXX.aiff")"
trap 'rm -f "$temporary_aiff"' EXIT

mkdir -p "$output_directory"
/usr/bin/say -v Samantha -r 190 -o "$temporary_aiff" \
  "The budget is approved. Send the contract today, and ask Morgan to confirm the delivery date."
/usr/bin/afconvert -f WAVE -d LEI16@16000 -c 1 "$temporary_aiff" "$output_path"

printf 'Generated public-safe local fixture: %s\n' "$output_path"
