#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${VOICE_LEDGER_PYTHON:-$ROOT/.venv/bin/python}"

export HF_HUB_OFFLINE="${HF_HUB_OFFLINE:-1}"
export TRANSFORMERS_OFFLINE="${TRANSFORMERS_OFFLINE:-1}"
export PORT="${PORT:-8788}"

exec "$PYTHON_BIN" "$ROOT/server.py"
