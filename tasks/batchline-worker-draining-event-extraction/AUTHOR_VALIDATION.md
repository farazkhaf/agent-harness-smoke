# Task validation — batchline-worker-draining-event-extraction 0.2.0

The task is validated with untouched-state, author-solution, and targeted mutation controls.

| Control | Expected result |
|---|---|
| untouched starting state | fail |
| author solution | G1-G6 pass |
| concrete worker schema retained in aggregate `$defs`, including under a renamed key | G5 fail |
| required worker schema definition removed | G5 fail |
| pure forwarding alias to the dedicated worker schema | pass |
| direct external worker `$ref` with a harmless generic sibling such as `type: object` | pass |
| extra test file or documentation edit | G6 fail |
| required schema-location test removed | G6 fail |
| split event-ID counter | G4 fail |
| duplicate worker constructor implementation retained in `encoder.py` | G4 fail |
| heartbeat `draining` made schema-required | fail |
| registry drain/resume changes preserved capacity or identity fields | G1/G2 fail |
| repository-native `make check` on the author solution | pass |

The current verifier is revision `r3`. The collection-time verifier and adjudication history are documented in `docs/provenance/scenario1_verifier_history.md`.
