import base64
import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

import server


class ServerContractTests(unittest.TestCase):
    def test_rejects_missing_audio(self):
        with self.assertRaises(server.ClientInputError):
            server._decode_audio({})

    def test_rejects_oversized_audio(self):
        payload = {"audioBase64": base64.b64encode(b"0" * (server.MAX_AUDIO_BYTES + 1)).decode("ascii")}
        with self.assertRaises(server.ClientInputError):
            server._decode_audio(payload)

    def test_uses_a_safe_source_name(self):
        audio, source = server._decode_audio({"audioBase64": base64.b64encode(b"wave").decode("ascii"), "sourceName": "../../note.wav"})
        self.assertEqual(audio, b"wave")
        self.assertEqual(source, "note.wav")

    def test_extracts_timestamped_words(self):
        result = {
            "segments": [
                {"start": 0, "end": 2, "words": [{"word": " Hello", "start": 0.1, "end": 0.4}, {"word": "world", "start": 0.5, "end": 0.9}]}
            ]
        }
        self.assertEqual(
            server._extract_words(result),
            [{"text": "Hello", "start": 0.1, "end": 0.4}, {"text": "world", "start": 0.5, "end": 0.9}],
        )

    def test_offline_mode_requires_both_flags(self):
        self.assertIsInstance(server.offline_mode(), bool)

    def test_listening_desk_exposes_local_source_playback(self):
        document = (server.WEB_ROOT / "index.html").read_text(encoding="utf-8")
        behavior = (server.WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (server.WEB_ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn('id="source-player"', document)
        self.assertIn("URL.createObjectURL(file)", behavior)
        self.assertIn("cueSource", behavior)
        self.assertIn("sourcePlayer.play()", behavior)
        self.assertIn("[hidden] { display: none !important; }", styles)

    def test_configures_a_private_ffmpeg_path(self):
        fake_module = type("FakeImageIoFfmpeg", (), {"get_ffmpeg_exe": staticmethod(lambda: "/private/ffmpeg")})
        with tempfile.TemporaryDirectory() as temporary_directory:
            fake_executable = Path(temporary_directory) / "ffmpeg-versioned"
            fake_executable.write_text("fake", encoding="utf-8")
            fake_module.get_ffmpeg_exe = staticmethod(lambda: str(fake_executable))
            with patch.dict("sys.modules", {"imageio_ffmpeg": fake_module}), patch.dict(os.environ, {"PATH": "/usr/bin"}, clear=False), patch.object(server, "ROOT", Path(temporary_directory)):
                server._configure_local_ffmpeg()
                alias = Path(temporary_directory) / ".tools" / "ffmpeg"
                self.assertTrue(alias.is_symlink())
                self.assertEqual(alias.resolve(), fake_executable.resolve())
                self.assertTrue(os.environ["PATH"].startswith(str(alias.parent)))


if __name__ == "__main__":
    unittest.main()
