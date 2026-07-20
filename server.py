"""A local-only WAV transcription server for Arm Voice Ledger.

The server deliberately uses the Python standard library for HTTP. The only
model dependency is the already-isolated Forge MLX Whisper environment.
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import resource
import tempfile
import time
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
WEB_ROOT = ROOT / "web"
MODEL_ID = os.environ.get("VOICE_LEDGER_MODEL", "mlx-community/whisper-tiny")
MAX_AUDIO_BYTES = 8 * 1024 * 1024
MAX_REQUEST_BYTES = 12 * 1024 * 1024


class ClientInputError(ValueError):
    """An input problem the listening desk can explain without a stack trace."""


def offline_mode() -> bool:
    return os.environ.get("HF_HUB_OFFLINE") == "1" and os.environ.get("TRANSFORMERS_OFFLINE") == "1"


def _peak_rss_bytes() -> int:
    # macOS reports ru_maxrss in bytes. Forge is the supported target surface.
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def _decode_audio(payload: dict[str, Any]) -> tuple[bytes, str]:
    encoded = payload.get("audioBase64")
    if not isinstance(encoded, str) or not encoded:
        raise ClientInputError("Choose a WAV file before transcribing.")
    try:
        audio = base64.b64decode(encoded, validate=True)
    except (ValueError, TypeError) as error:
        raise ClientInputError("The selected file could not be read as audio.") from error
    if not audio:
        raise ClientInputError("The selected WAV file is empty.")
    if len(audio) > MAX_AUDIO_BYTES:
        raise ClientInputError("Use a WAV smaller than 8 MB for this first local proof.")
    source_name = Path(str(payload.get("sourceName", "voice-note.wav"))).name or "voice-note.wav"
    return audio, source_name


def _extract_words(result: dict[str, Any]) -> list[dict[str, Any]]:
    words: list[dict[str, Any]] = []
    for segment in result.get("segments", []):
        for word in segment.get("words", []):
            text = str(word.get("word", "")).strip()
            if not text:
                continue
            words.append(
                {
                    "text": text,
                    "start": round(float(word.get("start", segment.get("start", 0))), 2),
                    "end": round(float(word.get("end", segment.get("end", 0))), 2),
                }
            )
    return words


def _configure_local_ffmpeg() -> None:
    """Expose imageio-ffmpeg's private binary to mlx-whisper's decoder."""
    try:
        import imageio_ffmpeg
    except ImportError as error:
        raise RuntimeError("The Forge audio decoder is not available.") from error
    executable = Path(imageio_ffmpeg.get_ffmpeg_exe())
    # imageio's bundled file is versioned, while mlx-whisper executes `ffmpeg`.
    # Keep the compatibility alias inside this disposable project, not on PATH
    # system-wide.
    tool_directory = ROOT / ".tools"
    tool_directory.mkdir(exist_ok=True)
    alias = tool_directory / "ffmpeg"
    if not alias.exists() and not alias.is_symlink():
        alias.symlink_to(executable)
    executable_directory = str(tool_directory)
    current_path = os.environ.get("PATH", "")
    if executable_directory not in current_path.split(os.pathsep):
        os.environ["PATH"] = f"{executable_directory}{os.pathsep}{current_path}"


def transcribe_local(audio: bytes, source_name: str) -> dict[str, Any]:
    """Run MLX Whisper and remove the temporary source audio before returning."""
    try:
        import mlx_whisper
    except ImportError as error:
        raise RuntimeError("The Forge MLX Whisper environment is not available.") from error

    _configure_local_ffmpeg()
    started = time.perf_counter()
    with tempfile.NamedTemporaryFile(prefix="voice-ledger-", suffix=".wav", delete=True) as temporary:
        temporary.write(audio)
        temporary.flush()
        result = mlx_whisper.transcribe(
            temporary.name,
            path_or_hf_repo=MODEL_ID,
            verbose=False,
            word_timestamps=True,
        )
    elapsed_ms = round((time.perf_counter() - started) * 1000)
    words = _extract_words(result)
    return {
        "sourceName": source_name,
        "transcript": str(result.get("text", "")).strip(),
        "words": words,
        "metrics": {
            "elapsedMs": elapsed_ms,
            "peakRssBytes": _peak_rss_bytes(),
            "model": MODEL_ID,
            "offlineModelCache": offline_mode(),
            "audioPersisted": False,
        },
    }


class VoiceLedgerHandler(SimpleHTTPRequestHandler):
    server_version = "ArmVoiceLedger/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        # Keep the terminal focused on model work and actual errors.
        return

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        request_path = urlparse(self.path).path
        if request_path == "/api/health":
            self._send_json(
                HTTPStatus.OK,
                {
                    "status": "ready",
                    "model": MODEL_ID,
                    "offlineModelCache": offline_mode(),
                    "audioPersisted": False,
                },
            )
            return

        relative_path = "index.html" if request_path in {"", "/"} else request_path.lstrip("/")
        candidate = (WEB_ROOT / relative_path).resolve()
        if WEB_ROOT not in candidate.parents and candidate != WEB_ROOT:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if not candidate.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = candidate.read_bytes()
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/transcribe":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        length_header = self.headers.get("Content-Length", "0")
        try:
            content_length = int(length_header)
        except ValueError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "The request size is invalid."})
            return
        if content_length <= 0 or content_length > MAX_REQUEST_BYTES:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Use a WAV smaller than 8 MB for this first local proof."})
            return
        try:
            payload = json.loads(self.rfile.read(content_length))
            if not isinstance(payload, dict):
                raise ClientInputError("The transcription request is malformed.")
            audio, source_name = _decode_audio(payload)
            self._send_json(HTTPStatus.OK, transcribe_local(audio, source_name))
        except ClientInputError as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except Exception as error:  # The raw provider error never enters the browser UI.
            print(f"transcription_failure={type(error).__name__}", flush=True)
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {
                    "error": "The local model could not finish this WAV. Keep the file, try a shorter WAV, and retry.",
                    "detail": type(error).__name__,
                },
            )


def main() -> None:
    port = int(os.environ.get("PORT", "8788"))
    server = ThreadingHTTPServer(("127.0.0.1", port), VoiceLedgerHandler)
    print(f"Arm Voice Ledger listening on http://127.0.0.1:{port}")
    print(f"model={MODEL_ID} offline_model_cache={offline_mode()} audio_persisted=false")
    server.serve_forever()


if __name__ == "__main__":
    main()
