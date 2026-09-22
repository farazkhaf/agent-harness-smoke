# V1 promotion provenance

The V1 canonical runs were executed against task metadata version `0.1.0-rc1`. After clearance, the task was promoted to `0.1.0` without changing the solver-visible instruction, verifier logic, workspace-observer logic, environment seed/setup, or oracle solution. Only version/release metadata and documentation changed; `tests/smoke_metadata.json` was updated to report the promoted task version.

The executed RC1 raw trials are retained outside the public release evidence surface. Public run receipts record the executed-to-published version mapping.

## Unchanged execution-content hashes

```text
7c53857acf3079f7f9088e232d9d4f5d3f2c6c068e833a82743d961f9f4159c8  tasks/batchline-shared-event-sequence-regression/instruction.md
c5e938eac091ae4a25d7ec8dd6692ebdc661c71d3457813234c1286230521f7f  tasks/batchline-shared-event-sequence-regression/tests/verify.py
4e103b5bfd1668c9b034be76908739607ee83a4d0ff30362d7bddcc75dafb9a2  tasks/batchline-shared-event-sequence-regression/tests/observe_workspace.py
aadd21d0b17f6a6a76fe3ae6fa8674b7489b051251152f7a62a0ca51d3209933  tasks/batchline-shared-event-sequence-regression/environment/Dockerfile
1e3617a62d8ff3da1f8c1e60e5f529351937776e839ad25f6334d9a0c16965e4  tasks/batchline-shared-event-sequence-regression/environment/setup/setup.sh
6a40e89fbcdec2979ccd43a76c6f56ce87d54447c6da7bb2ba71a91045698eb9  tasks/batchline-shared-event-sequence-regression/solution/solve.sh
```

Anchor seed commit: `f1ca22dae6f512a682496c227634a4368eeb940f`
