#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$DIR/providers.oracle.py" /app/src/batchline/execution/providers.py
cp "$DIR/test_providers.oracle.py" /app/tests/execution/test_providers.py
