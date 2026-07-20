#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VOICE_LEDGER_VENV:-$ROOT/.venv}"

"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r "$ROOT/requirements-forge.txt"

printf 'Environment ready: %s\n' "$VENV_DIR"
printf 'First run: HF_HUB_OFFLINE=0 TRANSFORMERS_OFFLINE=0 %s/scripts/run-forge.sh\n' "$ROOT"
printf 'Later runs default to the cached offline model.\n'
