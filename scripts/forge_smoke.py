"""Exercise the local HTTP route without preserving input audio."""

import base64
import argparse
import json
import os
import platform
import sys
import urllib.request
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def installed_version(package_name: str) -> str | None:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None


def build_receipt(result: dict, fixture: Path, base_url: str) -> dict:
    """Return the small, shareable record behind one local smoke run."""
    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(),
        "runtime": {
            "machine": platform.machine(),
            "platform": platform.platform(),
            "python": platform.python_version(),
            "endpoint": base_url,
        },
        "dependencies": {
            "mlx": installed_version("mlx"),
            "mlx-whisper": installed_version("mlx-whisper"),
            "imageio-ffmpeg": installed_version("imageio-ffmpeg"),
        },
        "input": {"fileName": fixture.name, "bytes": fixture.stat().st_size},
        "result": {
            "timestampedWords": len(result["words"]),
            "metrics": result["metrics"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Exercise the local Voice Ledger transcription route.")
    parser.add_argument("fixture", nargs="?", help="Path to a public-safe WAV fixture.")
    parser.add_argument(
        "--expect-online",
        action="store_true",
        help="Verify a deliberate first-run cache warm instead of the normal offline replay.",
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        help="Write a shareable JSON record of this local smoke run.",
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
    summary = {"words": len(result["words"]), "metrics": result["metrics"], "transcript": result["transcript"]}
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(build_receipt(result, fixture, base_url), indent=2) + "\n")
        summary["receipt"] = str(args.receipt)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
