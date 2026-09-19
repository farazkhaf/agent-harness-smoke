#!/usr/bin/env bash
set -euo pipefail
python - <<'PY'
from pathlib import Path
p=Path('/app/config/job-policies.toml')
s=p.read_text()
for name in ['thumbnail','billing_export','daily_digest']:
    header=f'[jobs.{name}]'
    start=s.index(header)
    end=s.find('\n[jobs.', start+1)
    if end == -1: end=len(s)
    chunk=s[start:end]
    chunk=chunk.replace('retry_policy = "standard"','retry_policy = "aggressive"',1)
    s=s[:start]+chunk+s[end:]
p.write_text(s)
PY
