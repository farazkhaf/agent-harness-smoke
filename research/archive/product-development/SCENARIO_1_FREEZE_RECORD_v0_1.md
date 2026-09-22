# Scenario 1 freeze record — task 0.2.0

Frozen task: `agent-harness-smoke/batchline-worker-draining-event-extraction` `0.2.0`  
Freeze date: 2026-09-21

## Clearance evidence

The final RC2 candidate was cleared before version promotion:

- Harbor NOP: reward `0`; prerequisite-dependent groups may report `blocked` after earlier required lifecycle surfaces are absent. This is intentional cascade suppression, not an indeterminate verifier state.
- Harbor oracle: reward `1`; G1-G6 pass.
- matched OpenCode 1.18.30 / GLM-5p3-flash task-design diagnostic: reward `1`; G1-G6 pass.
- diagnostic workload review found the intended pressure concentrated in distributed lifecycle coordination, Python event extraction, large structured worker-schema extraction/selective preservation and bounded verification; no further task redesign was required.

The NOP/oracle controls and diagnostic are authoring/clearance evidence, not formal scenario comparison runs.

## Freeze promotion changes

No solver-facing software requirement was changed after clearance.

The following candidate components are byte-identical at freeze:

- `instruction.md` SHA-256: `4ea48fc5f57070d49d984d47d96c8d1d13061399e92e046744a20593a4102d5c`
- `tests/verify.py` SHA-256: `5eb7c60a55f9f985a811c9948081d063eef428cadd1b9a4abb596b736091c737`
- `environment/Dockerfile` SHA-256: `aadd21d0b17f6a6a76fe3ae6fa8674b7489b051251152f7a62a0ca51d3209933`
- seed repository tree digest (97 files, SHA-256 over sorted relative-path/file-hash rows): `46eb9b94ac59483f77fb12d0325f6a1c9678dce954f0fd670aa110f39c4e92d0`; identical to the cleared RC2 candidate.

Freeze-only changes are:

- task version metadata `0.2.0-rc1` → `0.2.0`;
- descriptive observer schema `0.1` → `0.2` to separate tracked diff lines from untracked text-file lines;
- reporting support for the new descriptive observer fields;
- post-clearance evaluation/provenance documentation;
- archival relocation of authoring/clearance notes.

The observer remains non-scoring and runs before the verifier. Its legacy `changed_files`, `lines_added`, `lines_deleted` and `untracked_files` fields retain their previous meanings.

## Solver-visible leakage audit

The task environment Dockerfile copies only `environment/repo/` into `/app`. Task authoring notes, oracle solution, verifier implementation and evaluation documents are not copied into the agent workspace.

Audit results:

- `instruction.md` contains no pre-freeze/clearance/authoring/pressure/RC terminology;
- the seed repository contains no scenario/task-design/clearance language; ordinary product uses of words such as `diagnostic` are unrelated application terminology;
- no oracle/design rationale comments were embedded in the seed product code;
- build-only setup material is removed after image setup.

Task metadata identifies the task as a scenario, which is benchmark metadata rather than hidden design rationale.

## Workspace footprint instrumentation

Observer `0.2` uses:

- tracked modifications: `git diff --numstat <baseline> --`;
- untracked files: `git ls-files --others --exclude-standard`;
- UTF-8 text-line counts for those untracked files;
- separate listing of untracked binary files.

`--exclude-standard` respects `.gitignore` and standard Git exclude files, so cache/build artifacts such as `__pycache__/`, `.pytest_cache/`, bytecode, build/dist and egg-info paths are excluded when ignored by the repository.

A local oracle observer check using schema `0.2` reports 10 tracked changed files, 4 untracked text files, tracked `+93/-374`, untracked text `+508`, and combined text footprint `+601/-374`, with zero unexpected/forbidden paths. This matches the author-side oracle patch calibration and validates the new decomposition.

A final Git commit is deliberately **not** a task requirement: committing would introduce a separate VCS interaction requirement without improving contract correctness.

## P2P/F2P convention

The frozen verifier remains the cleared G1-G6 implementation. P2P/F2P roles are documented at requirement level in the task-local `VERIFICATION_ROLE_MAP.md`; no post-clearance verifier split was introduced solely for formatting consistency.

## Next boundary

The task is frozen, but formal scenario collection has not started. Lock the harness/repeat/evidence matrix prospectively before the first formal run using `SCENARIO_1_FORMAL_RUN_PROTOCOL_v0_2.md` or a finalized successor.
