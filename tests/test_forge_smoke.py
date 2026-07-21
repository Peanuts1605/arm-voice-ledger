import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "forge_smoke.py"
SPEC = importlib.util.spec_from_file_location("forge_smoke", SCRIPT_PATH)
assert SPEC and SPEC.loader
forge_smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(forge_smoke)


class ForgeSmokeReceiptTests(unittest.TestCase):
    def test_build_receipt_records_runtime_input_and_model_metrics(self):
        result = {
            "words": [{"text": "Ready", "start": 0, "end": 0.3}],
            "metrics": {
                "elapsedMs": 123,
                "peakRssBytes": 456,
                "model": "mlx-community/whisper-tiny",
                "offlineModelCache": True,
                "audioPersisted": False,
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "proof.wav"
            fixture.write_bytes(b"synthetic")
            receipt = forge_smoke.build_receipt(result, fixture, "http://127.0.0.1:8788")

        self.assertEqual(receipt["schemaVersion"], 1)
        self.assertEqual(receipt["input"], {"fileName": "proof.wav", "bytes": 9})
        self.assertEqual(receipt["result"]["timestampedWords"], 1)
        self.assertTrue(receipt["result"]["metrics"]["offlineModelCache"])
        self.assertFalse(receipt["result"]["metrics"]["audioPersisted"])
        self.assertEqual(receipt["runtime"]["endpoint"], "http://127.0.0.1:8788")


if __name__ == "__main__":
    unittest.main()
