from datetime import UTC, datetime
from pathlib import Path
import hashlib
import json

APP = Path('/app')
ARCHIVE = APP / 'operations/incident-2026-08-14.jsonl'
OUTPUT = APP / 'operations/quarantine-events.txt'
START = datetime(2026, 8, 14, 2, 0, tzinfo=UTC)
END = datetime(2026, 8, 14, 2, 40, tzinfo=UTC)


def fail(message: str) -> None:
    print(f'FAIL: {message}')
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def expected_event_ids() -> tuple[str, ...]:
    """Compute the expected quarantine list without importing workspace code."""
    matches: list[tuple[str, str]] = []
    with ARCHIVE.open('r', encoding='utf-8') as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                event = json.loads(text)
            except json.JSONDecodeError as exc:
                fail(f'incident archive contains invalid JSON at line {line_number}: {exc.msg}')
            if not isinstance(event, dict):
                fail(f'incident archive line {line_number} is not a JSON object')
            if event.get('worker') != 'worker-05':
                continue
            if event.get('event_type') != 'worker.rate_limited':
                continue
            if event.get('provider') != 'images-api':
                continue
            try:
                occurred_text = str(event['occurred_at'])
                occurred = datetime.fromisoformat(occurred_text.replace('Z', '+00:00'))
                event_id = str(event['event_id'])
            except (KeyError, ValueError) as exc:
                fail(f'incident archive line {line_number} is missing required event data: {exc}')
            if START <= occurred <= END:
                matches.append((occurred_text, event_id))
    matches.sort()
    return tuple(event_id for _, event_id in matches)


def main() -> None:
    expected_sha = Path('/tests/archive.sha256').read_text().strip()
    if sha256(ARCHIVE) != expected_sha:
        fail('incident archive was modified')

    expected = expected_event_ids()
    if not OUTPUT.exists():
        fail('quarantine output file is missing')
    actual = tuple(line.strip() for line in OUTPUT.read_text(encoding='utf-8').splitlines() if line.strip())
    if actual != expected:
        fail(f'quarantine list mismatch: expected {expected}, got {actual}')
    if len(actual) != 10:
        fail(f'expected 10 quarantine events, got {len(actual)}')
    print('PASS')


if __name__ == '__main__':
    main()
