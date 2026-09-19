from pathlib import Path
import subprocess
import sys
import tomllib
import os

APP = Path('/app')
POLICY = APP / 'config' / 'job-policies.toml'
TARGETS = {'thumbnail', 'billing_export', 'daily_digest'}


def fail(message: str) -> None:
    print(f'FAIL: {message}')
    raise SystemExit(1)


def main() -> None:
    try:
        current = tomllib.loads(POLICY.read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f'job policy catalog is not valid TOML: {exc}')
    baseline = tomllib.loads(Path('/tests/baseline-job-policies.toml').read_text(encoding='utf-8'))
    expected = baseline
    for name in TARGETS:
        expected['jobs'][name]['retry_policy'] = 'aggressive'
    if current != expected:
        fail('job policy settings differ from the required selective update')

    result = subprocess.run(
        [sys.executable, 'tools/validate_policies.py'],
        cwd=APP,
        env={**os.environ, 'PYTHONPATH': '/app/src'},
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        fail(f'policy validation failed: {result.stdout}{result.stderr}')
    print('PASS')


if __name__ == '__main__':
    main()
