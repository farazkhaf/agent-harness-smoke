#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$DIR/providers.oracle.py" /app/src/batchline/execution/providers.py
cp "$DIR/legacy_remote.oracle.py" /app/src/batchline/execution/legacy_remote.py
