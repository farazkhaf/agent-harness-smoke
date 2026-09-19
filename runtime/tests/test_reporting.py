from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUNTIME / "report"))
sys.path.insert(0, str(RUNTIME / "suite"))

from report_trial import normalize_trial, write_report  # noqa: E402
from suite_config import execution_plan, load_suite  # noqa: E402
from collect_suite import aggregate, enrich, load_reports  # noqa: E402


class ReportingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(__file__).resolve().parents[2]
        self.suite_path = self.repo / "suites" / "batchline-focused" / "suite.toml"

    def _write_trial(self, root: Path, name: str, task_id: str, calls: int = 4) -> Path:
        trial = root / name
        (trial / "agent").mkdir(parents=True)
        result = {
            "id": name,
            "trial_name": name,
            "task_name": task_id,
            "task_checksum": "abc123",
            "config": {
                "agent": {"import_path": "example:Agent", "model_name": "provider/model"},
                "task": {"path": task_id},
            },
            "agent_info": {
                "name": "example-harness",
                "version": "1.2.3",
                "model_info": {"provider": "provider", "name": "model"},
            },
            "agent_result": {
                "n_input_tokens": 1000,
                "n_cache_tokens": 400,
                "n_output_tokens": 100,
                "cost_usd": 0.01,
                "metadata": None,
            },
            "verifier_result": {"rewards": {"reward": 1.0, "behavior": 1.0}},
            "exception_info": None,
            "started_at": "2026-09-17T00:00:00Z",
            "finished_at": "2026-09-17T00:00:10Z",
            "environment_setup": {"started_at": "2026-09-17T00:00:00Z", "finished_at": "2026-09-17T00:00:02Z"},
            "agent_setup": {"started_at": "2026-09-17T00:00:02Z", "finished_at": "2026-09-17T00:00:03Z"},
            "agent_execution": {"started_at": "2026-09-17T00:00:03Z", "finished_at": "2026-09-17T00:00:09Z"},
            "verifier": {"started_at": "2026-09-17T00:00:09Z", "finished_at": "2026-09-17T00:00:10Z"},
        }
        (trial / "result.json").write_text(json.dumps(result), encoding="utf-8")
        trajectory = {
            "schema_version": "ATIF-v1.7",
            "steps": [{"llm_call_count": 1} for _ in range(calls)],
            "final_metrics": {"total_steps": calls + 1},
        }
        (trial / "agent" / "trajectory.json").write_text(json.dumps(trajectory), encoding="utf-8")
        return trial

    def test_public_report_is_compact_and_atif_only_supplies_call_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            trial = self._write_trial(Path(tmp), "trial-a", "agent-harness-smoke/batchline-submitted-by", calls=4)
            report = normalize_trial(trial)
            self.assertEqual(report["telemetry"]["inference_calls"], 4)
            self.assertEqual(report["telemetry"]["inference_calls_source"], "harbor_atif")
            self.assertEqual(report["telemetry"]["uncached_input_tokens"], 600)
            self.assertNotIn("workspace", report)
            self.assertNotIn("reasoning_tokens", report["telemetry"])
            self.assertNotIn("first_call_prompt_tokens", report["telemetry"])
            self.assertEqual(report["outcome"]["rewards"]["behavior"], 1.0)

    def test_focused_suite_is_five_tasks_by_two_profiles(self) -> None:
        suite = load_suite(self.suite_path)
        self.assertEqual(suite["schema_version"], "0.2")
        self.assertEqual(len(suite["tasks"]), 5)
        self.assertEqual(len(suite["profiles"]), 2)
        plan = execution_plan(suite)
        self.assertEqual(len(plan), 10)
        self.assertEqual({entry["execution"] for entry in plan}, {"preinstalled"})
        ids = {t["id"] for t in suite["tasks"]}
        self.assertNotIn("agent-harness-smoke/batchline-rate-limit-retry-after", ids)
        for task in suite["tasks"]:
            self.assertTrue((self.repo / task["path"] / "task.toml").is_file())

    def test_external_profile_plan_does_not_require_runtime_image_or_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            suite_path = Path(tmp) / "suite.toml"
            suite_path.write_text(
                '''schema_version = "0.2"
id = "private-local"
kind = "focused-task"
description = "external profile smoke"
repeats = 1

[[tasks]]
id = "agent-harness-smoke/batchline-submitted-by"
version = "0.1.0"
path = "tasks/batchline-submitted-by"

[[profiles]]
id = "private-dev"
execution = "external"
agent = "my_harness.harbor_adapter:PrivateHarnessAgent"
''',
                encoding="utf-8",
            )
            suite = load_suite(suite_path)
            plan = execution_plan(suite)
            self.assertEqual(len(plan), 1)
            self.assertEqual(plan[0]["execution"], "external")
            self.assertEqual(plan[0]["agent"], "my_harness.harbor_adapter:PrivateHarnessAgent")
            self.assertIsNone(plan[0]["runtime_profile"])
            self.assertIsNone(plan[0]["model"])

    def test_external_profile_requires_agent_import_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            suite_path = Path(tmp) / "suite.toml"
            suite_path.write_text(
                '''schema_version = "0.2"
id = "bad-external"
kind = "focused-task"
description = "invalid external profile"

[[tasks]]
id = "agent-harness-smoke/batchline-submitted-by"
path = "tasks/batchline-submitted-by"

[[profiles]]
id = "private-dev"
execution = "external"
''',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "requires agent import path"):
                load_suite(suite_path)

    def test_collector_reads_normalized_reports_and_aggregates_repeats(self) -> None:
        suite = load_suite(self.suite_path)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for attempt in (1, 2):
                trial = self._write_trial(root, f"trial-{attempt}", "agent-harness-smoke/batchline-submitted-by", calls=attempt + 2)
                report = normalize_trial(trial)
                out = root / "reports" / "faraz_batchline-submitted-by" / "example" / f"attempt-{attempt}"
                write_report(report, out)
            reports = load_reports(root / "reports")
            rows = [enrich(r, suite) for r in reports]
            self.assertEqual({r["attempt"] for r in rows}, {1, 2})
            summary = aggregate(rows)
            self.assertEqual(len(summary), 1)
            self.assertEqual(summary[0]["runs"], 2)
            self.assertEqual(summary[0]["pass_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
