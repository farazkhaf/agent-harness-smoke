# Validation

The release was validated at three levels.

## Task controls

Each task includes a failing untouched-state control and a passing author solution. Task-specific `AUTHOR_VALIDATION.md` files record additional negative controls, verifier sensitivity checks, and repository validation.

## Runtime and reporting controls

- Mini-SWE-Agent 2.4.6 and OpenCode 1.18.30 were exercised through version-pinned reusable runtime images and thin Harbor wrappers.
- The generic task binder preserves task content apart from runtime binding metadata and base-image substitution.
- Reporting and suite regression tests pass.
- Task, suite, and profile TOML files parse successfully.

## Formal focused matrix

The canonical matrix contains 15 Harbor runs: five tasks across OpenCode, Mini-SWE, and `custom-harness`. All 15 rows pass with `reward = 1.0`.

R2 and R3 use task version 0.1.1 after verifier corrections. B1, R1, and R4 use version 0.1.0.

The release includes trajectory evidence for the ten OpenCode and Mini-SWE rows and normalized result fields for all 15 rows.
