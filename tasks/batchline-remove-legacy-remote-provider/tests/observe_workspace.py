import argparse
import fnmatch
import json
from pathlib import Path
import subprocess


def run_git(*args: str) -> str:
    return subprocess.check_output(['git', '-C', '/app', *args], text=True).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    metadata = json.loads(Path(args.metadata).read_text())
    baseline = Path('/opt/smoke-baseline-sha').read_text().strip()

    names = [x for x in run_git('diff', '--name-only', baseline, '--').splitlines() if x]
    status_lines = [x for x in run_git('status', '--porcelain').splitlines() if x]
    untracked = [line[3:] for line in status_lines if line.startswith('?? ')]

    added = deleted = 0
    numstat = run_git('diff', '--numstat', baseline, '--')
    for line in numstat.splitlines():
        if not line:
            continue
        a, d, _ = line.split('\t', 2)
        if a.isdigit():
            added += int(a)
        if d.isdigit():
            deleted += int(d)

    expected = metadata.get('expected_edit_globs', [])
    forbidden = metadata.get('forbidden_edit_globs', [])

    def matches_any(path: str, patterns: list[str]) -> bool:
        return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)

    unexpected = [
        path for path in names
        if expected and not matches_any(path, expected)
    ]
    forbidden_changed = [path for path in names if matches_any(path, forbidden)]

    result = {
        'schema_version': '0.1',
        'observer': 'git',
        'baseline_ref': baseline,
        'changed_files': len(names),
        'changed_paths': names,
        'lines_added': added,
        'lines_deleted': deleted,
        'untracked_files': len(untracked),
        'untracked_paths': untracked,
        'unexpected_files_changed': len(unexpected),
        'unexpected_paths': unexpected,
        'forbidden_files_changed': len(forbidden_changed),
        'forbidden_paths': forbidden_changed,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
