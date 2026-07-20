"""Exercise the local HTTP route without preserving input audio."""

import base64
import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Exercise the local Voice Ledger transcription route.")
    parser.add_argument("fixture", nargs="?", help="Path to a public-safe WAV fixture.")
    parser.add_argument(
        "--expect-online",
        action="store_true",
        help="Verify a deliberate first-run cache warm instead of the normal offline replay.",
    )
    args = parser.parse_args()
    default_fixture = Path(__file__).resolve().parent.parent / "demo" / "synthetic-forge-fixture.wav"
    fixture = Path(args.fixture) if args.fixture else default_fixture
    if not fixture.is_file():
        raise SystemExit(
            "Pass a public-safe WAV path: python scripts/forge_smoke.py /path/to/fixture.wav"
        )
    payload = json.dumps(
        {"sourceName": "synthetic-forge-fixture.wav", "audioBase64": base64.b64encode(fixture.read_bytes()).decode("ascii")}
    ).encode("utf-8")
    base_url = os.environ.get("VOICE_LEDGER_URL", "http://127.0.0.1:8788").rstrip("/")
    request = urllib.request.Request(
        f"{base_url}/api/transcribe",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)
    expected_offline = not args.expect_online
    assert result["metrics"]["offlineModelCache"] is expected_offline
    assert result["metrics"]["audioPersisted"] is False
    assert len(result["words"]) > 0
    print(json.dumps({"words": len(result["words"]), "metrics": result["metrics"], "transcript": result["transcript"]}, indent=2))


if __name__ == "__main__":
    main()
