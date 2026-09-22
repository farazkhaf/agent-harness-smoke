import argparse
import fnmatch
import json
import os
from pathlib import Path
import subprocess


APP = Path(os.environ.get("BATCHLINE_APP", "/app")).resolve()
BASELINE_FILE = Path(os.environ.get("HARNESS_SMOKE_BASELINE_FILE", "/opt/smoke-baseline-sha"))


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(APP), *args], text=True).strip()


def text_line_count(path: Path) -> int | None:
    """Return text-line count for an untracked file, or None for binary/unreadable content."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data:
        return None
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    metadata = json.loads(Path(args.metadata).read_text())
    baseline = BASELINE_FILE.read_text().strip()

    tracked_paths = [x for x in run_git("diff", "--name-only", baseline, "--").splitlines() if x]
    # --exclude-standard respects repository .gitignore, .git/info/exclude and the user's
    # standard Git excludes. This keeps caches/build products out while retaining genuine
    # newly created task files.
    untracked_paths = [x for x in run_git("ls-files", "--others", "--exclude-standard").splitlines() if x]

    tracked_added = tracked_deleted = 0
    tracked_numstat: dict[str, dict[str, int | None]] = {}
    numstat = run_git("diff", "--numstat", baseline, "--")
    for line in numstat.splitlines():
        if not line:
            continue
        a, d, path = line.split("\t", 2)
        a_num = int(a) if a.isdigit() else None
        d_num = int(d) if d.isdigit() else None
        if a_num is not None:
            tracked_added += a_num
        if d_num is not None:
            tracked_deleted += d_num
        tracked_numstat[path] = {"added": a_num, "deleted": d_num}

    untracked_text_line_map: dict[str, int] = {}
    untracked_binary_paths: list[str] = []
    for rel in untracked_paths:
        count = text_line_count(APP / rel)
        if count is None:
            untracked_binary_paths.append(rel)
        else:
            untracked_text_line_map[rel] = count

    untracked_text_added = sum(untracked_text_line_map.values())
    all_changed_paths = sorted(set(tracked_paths) | set(untracked_paths))

    expected = metadata.get("expected_edit_globs", [])
    forbidden = metadata.get("forbidden_edit_globs", [])

    def matches_any(path: str, patterns: list[str]) -> bool:
        return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)

    unexpected = [path for path in all_changed_paths if expected and not matches_any(path, expected)]
    forbidden_changed = [path for path in all_changed_paths if matches_any(path, forbidden)]

    result = {
        "schema_version": "0.2",
        "observer": "git",
        "baseline_ref": baseline,
        # Backward-compatible tracked-diff fields used by the existing reporter.
        "changed_files": len(tracked_paths),
        "changed_paths": tracked_paths,
        "lines_added": tracked_added,
        "lines_deleted": tracked_deleted,
        "untracked_files": len(untracked_paths),
        "untracked_paths": untracked_paths,
        # Explicit footprint decomposition for scenario analysis.
        "tracked_changed_files": len(tracked_paths),
        "tracked_changed_paths": tracked_paths,
        "tracked_lines_added": tracked_added,
        "tracked_lines_deleted": tracked_deleted,
        "tracked_numstat": tracked_numstat,
        "untracked_text_files": len(untracked_text_line_map),
        "untracked_text_lines_added": untracked_text_added,
        "untracked_text_line_map": untracked_text_line_map,
        "untracked_binary_files": len(untracked_binary_paths),
        "untracked_binary_paths": untracked_binary_paths,
        "workspace_changed_files_total": len(all_changed_paths),
        "workspace_changed_paths_total": all_changed_paths,
        "workspace_text_lines_added_total": tracked_added + untracked_text_added,
        "workspace_text_lines_deleted_total": tracked_deleted,
        "unexpected_files_changed": len(unexpected),
        "unexpected_paths": unexpected,
        "forbidden_files_changed": len(forbidden_changed),
        "forbidden_paths": forbidden_changed,
        "line_count_note": (
            "lines_added/lines_deleted are tracked git diff --numstat values for backward compatibility. "
            "workspace_text_lines_added_total additionally counts UTF-8 text lines in untracked files returned by "
            "git ls-files --others --exclude-standard; ignored files and binary untracked files are excluded from that total."
        ),
        "note": "Descriptive workspace evidence only; observer fields do not determine scenario reward.",
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
