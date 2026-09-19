#!/usr/bin/env bash
set -euo pipefail

SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The preinstalled agent images already contain these ordinary repository-work
# tools. The standalone canonical task base is intentionally thinner, so fill
# only genuinely missing repo prerequisites here.
missing=()
command -v git >/dev/null 2>&1 || missing+=(git)
command -v make >/dev/null 2>&1 || missing+=(make)
if (( ${#missing[@]} > 0 )); then
    command -v apt-get >/dev/null 2>&1 || { echo "Missing repo prerequisites: ${missing[*]}; runtime has no apt-get" >&2; exit 2; }
    apt-get update
    apt-get install -y --no-install-recommends "${missing[@]}"
    rm -rf /var/lib/apt/lists/*
fi

python -m pip install --no-cache-dir -r "$SETUP_DIR/requirements-lock.txt"

cd /app
PYTHONPATH=/app/src python tools/generate_event_archive.py operations/incident-2026-08-14.jsonl --count 18000
rm -rf .git
git init -q
git config user.email "smoke@example.invalid"
git config user.name "Harness Task"
git add .
git commit -q -m "baseline"
git rev-parse HEAD > /opt/smoke-baseline-sha

# Build-only setup material should not remain in the task workspace/image.
rm -rf "$SETUP_DIR"
