from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile

APP = Path('/app')
TEST = APP / 'tests/events/test_event_sequence.py'
ENCODER = APP / 'src/batchline/events/encoder.py'
ALLOWED = {
    'src/batchline/events/encoder.py',
    'tests/events/test_event_sequence.py',
}


def fail(message: str) -> None:
    print(f'FAIL: {message}')
    raise SystemExit(1)


def run(cmd: list[str], *, cwd: Path = APP, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env={**os.environ, 'PYTHONPATH': str(cwd / 'src')},
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        fail(f'command failed: {cmd}\n{result.stdout}{result.stderr}')
    return result


def changed_paths() -> set[str]:
    baseline = Path('/opt/smoke-baseline-sha').read_text().strip()
    tracked = subprocess.check_output(
        ['git', '-C', str(APP), 'diff', '--name-only', baseline, '--'], text=True
    ).splitlines()
    status = subprocess.check_output(
        ['git', '-C', str(APP), 'status', '--porcelain'], text=True
    ).splitlines()
    untracked = [line[3:] for line in status if line.startswith('?? ')]
    return {p for p in tracked + untracked if p}


def numeric_suffix(event_id: str) -> int:
    try:
        return int(event_id.rsplit('_', 1)[1])
    except (IndexError, ValueError) as exc:
        fail(f'event id has no numeric suffix: {event_id!r}')
        raise AssertionError from exc


def verify_runtime_behavior() -> None:
    sys.path.insert(0, str(APP / 'src'))
    from batchline.config.models import ServiceConfig
    from batchline.events.encoder import (
        job_event,
        service_config_loaded_event,
        worker_heartbeat_event,
    )
    from batchline.jobs.models import Job
    from batchline.workers.models import WorkerSnapshot

    fixed = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    job = Job(
        id='job-sequence-verify',
        kind='thumbnail',
        queue='media',
        created_at=fixed,
        updated_at=fixed,
    )
    worker = WorkerSnapshot(
        name='thumb-sequence-verify',
        service='thumbnailer',
        queue='media',
        last_seen_at=fixed,
        active_jobs=1,
        capacity=4,
    )
    config = ServiceConfig(
        name='thumbnailer',
        queue='media',
        concurrency=4,
        timeout_seconds=120,
        max_retries=4,
        enabled=True,
    )

    ids = [
        job_event(job, occurred_at=fixed).event_id,
        worker_heartbeat_event(worker, occurred_at=fixed).event_id,
        service_config_loaded_event(config, environment='verify', occurred_at=fixed).event_id,
        job_event(job, occurred_at=fixed).event_id,
    ]
    numbers = [numeric_suffix(value) for value in ids]
    expected = list(range(numbers[0], numbers[0] + len(numbers)))
    if numbers != expected:
        fail(f'event families do not share one monotonic sequence: ids={ids}, suffixes={numbers}')


def run_submitted_test(repo: Path) -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            '-m',
            'pytest',
            '-q',
            'tests/events/test_event_sequence.py::test_event_id_sequence_is_shared_across_families',
        ],
        cwd=repo,
    )


def baseline_repo_with_submitted_test(root: Path) -> Path:
    baseline = Path('/opt/smoke-baseline-sha').read_text().strip()
    repo = root / 'baseline'
    repo.mkdir()
    archive = subprocess.Popen(
        ['git', '-C', str(APP), 'archive', baseline],
        stdout=subprocess.PIPE,
    )
    extract = subprocess.run(['tar', '-x', '-C', str(repo)], stdin=archive.stdout)
    assert archive.stdout is not None
    archive.stdout.close()
    archive_rc = archive.wait()
    if archive_rc != 0 or extract.returncode != 0:
        fail('could not materialize baseline repository for regression-test validation')
    destination = repo / 'tests/events/test_event_sequence.py'
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEST, destination)
    return repo


def run_submitted_test_after_preconsumption(repo: Path) -> subprocess.CompletedProcess[str]:
    script = r"""
from datetime import UTC, datetime
import sys
import pytest
from batchline.jobs.models import Job
from batchline.events.encoder import job_event

fixed = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
job = Job(id='preconsume', kind='thumbnail', queue='media', created_at=fixed, updated_at=fixed)
for _ in range(11):
    job_event(job, occurred_at=fixed)
raise SystemExit(pytest.main(['-q', 'tests/events/test_event_sequence.py::test_event_id_sequence_is_shared_across_families']))
"""
    return run([sys.executable, '-c', script], cwd=repo)


def main() -> None:
    paths = changed_paths()
    if paths != ALLOWED:
        fail(f'task scope changed unexpectedly: expected {sorted(ALLOWED)}, got {sorted(paths)}')
    if not TEST.exists():
        fail('required regression test file is missing')
    if not ENCODER.exists():
        fail('encoder.py is missing')

    candidate_test = run_submitted_test(APP)
    if candidate_test.returncode != 0:
        fail(f'required regression test does not pass on the submitted solution:\n{candidate_test.stdout}{candidate_test.stderr}')

    verify_runtime_behavior()

    with tempfile.TemporaryDirectory(prefix='batchline-sequence-verify-') as temp:
        root = Path(temp)
        baseline_repo = baseline_repo_with_submitted_test(root)
        baseline_result = run_submitted_test(baseline_repo)
        if baseline_result.returncode == 0:
            fail('submitted regression test does not detect the seeded per-prefix sequence bug')

        preconsumed = run_submitted_test_after_preconsumption(APP)
        if preconsumed.returncode != 0:
            fail(
                'submitted regression test appears to assume a fixed initial sequence value; '
                'it must still pass after earlier events have consumed sequence values in the same process:\n'
                f'{preconsumed.stdout}{preconsumed.stderr}'
            )

    full = run(['make', 'check'])
    if full.returncode != 0:
        fail(f'repository validation failed (`make check`):\n{full.stdout}{full.stderr}')

    print('PASS')


if __name__ == '__main__':
    main()
