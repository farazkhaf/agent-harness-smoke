from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

RUNTIME = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUNTIME))

from bind_task import bind_task  # noqa: E402


class BindTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(__file__).resolve().parents[2]
        self.task = self.repo / "tasks" / "batchline-submitted-by"

    def test_mini_swe_binding_changes_only_base_default(self) -> None:
        profile = self.repo / "runtime" / "profiles" / "mini-swe-2.4.6.yaml"
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "resolved"
            binding = bind_task(self.task, profile, output)
            dockerfile = (output / "environment" / "Dockerfile").read_text()
            self.assertIn("ARG HARNESS_SMOKE_BASE_IMAGE=harness-smoke/mini-swe:2.4.6", dockerfile)
            self.assertTrue((output / "environment" / "setup" / "setup.sh").is_file())
            self.assertEqual(binding["integration"], "harness_smoke_agents.preinstalled_mini_swe:PreinstalledMiniSweAgent")
            saved = json.loads((output / ".harness-smoke-binding.json").read_text())
            self.assertEqual(saved["runtime_profile_id"], "mini-swe-2.4.6")

    def test_opencode_binding(self) -> None:
        profile = self.repo / "runtime" / "profiles" / "opencode-1.18.30.yaml"
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "resolved"
            binding = bind_task(self.task, profile, output)
            dockerfile = (output / "environment" / "Dockerfile").read_text()
            self.assertIn("ARG HARNESS_SMOKE_BASE_IMAGE=harness-smoke/opencode:1.18.30", dockerfile)
            self.assertEqual(binding["runtime_profile_id"], "opencode-1.18.30")

    def test_binding_preserves_task_content(self) -> None:
        profile = self.repo / "runtime" / "profiles" / "mini-swe-2.4.6.yaml"
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "resolved"
            bind_task(self.task, profile, output)
            self.assertTrue((output / "environment" / "setup" / "requirements-lock.txt").is_file())
            self.assertTrue((output / "tests" / "verify.py").is_file())
            self.assertEqual(
                (output / "instruction.md").read_text(),
                (self.task / "instruction.md").read_text(),
            )


if __name__ == "__main__":
    unittest.main()
