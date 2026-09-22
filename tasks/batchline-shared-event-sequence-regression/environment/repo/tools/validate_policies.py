#!/usr/bin/env python
from __future__ import annotations

from batchline.policies import load_job_policies


def main() -> int:
    catalog = load_job_policies()
    print(f"validated {len(catalog)} job policies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
