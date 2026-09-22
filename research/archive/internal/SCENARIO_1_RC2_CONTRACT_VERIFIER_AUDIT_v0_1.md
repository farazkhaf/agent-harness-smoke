# Scenario 1 RC2 contract/verifier audit — v0.1

Internal authoring audit. Verifier requirements below are traceable to solver-visible contract clauses; author-only patch-size/tool-route calibration is intentionally absent.

| Contract surface | Verifier group | Verification form |
|---|---|---|
| drain/resume state invariants and immutable transitions | G1 | behavioral |
| registry drain/resume persistence | G1 | behavioral |
| draining-aware capacity and heartbeat-health independence | G2 | behavioral |
| serializer state/reason fields | G3 | behavioral |
| CLI STATE/REASON and command messages | G3 | behavioral/public text |
| `worker_events.py` owns five named constructors | G4 | stated structural ownership + identity/source checks |
| `encoder.py` compatibility exports without duplicate/proxy definitions | G4 | stated structural/identity checks |
| one shared worker/non-worker event-ID sequence | G4 | same-process behavioral probe after earlier IDs are consumed |
| heartbeat draining compatibility | G5 | behavior + schema validation, legacy fixture remains valid |
| draining-event reason compatibility | G5 | behavioral |
| resumed event payload/registration/strict schema/example | G5 | behavioral/schema/example |
| `worker-events.schema.json` owns five explicitly named worker definitions | G5 | stated schema ownership + schema validity |
| aggregate schema no longer owns concrete worker definitions | G5 | stated structural ownership |
| aggregate keeps job/service event ownership | G5 | event-type behavior, not oracle definition-name spelling |
| aggregate worker variants reference `worker-events.schema.json` | G5 | URI-suffix target check; relative or equivalent absolute URI accepted |
| aggregate validation transparently resolves worker schema | G5/G6 | normal `validate_event`, example validation, `make check` |
| registry/schema parity across split files | G5 | behavioral helper result/type discovery |
| dedicated worker schema independently validates worker events | G5 | Draft 2020-12 direct validation |
| named existing schema-location test updated; other two validation tests retained | G6 | explicitly named test functions + native test run |
| no other test files/docs in final change | G6 | normative Git scope check because contract explicitly forbids them |
| full lifecycle and repository preservation | G6 | integration + `make check` |

## Anti-oracle controls

- Equivalent absolute worker-schema reference URIs pass.
- Internal shared-helper layout remains unspecified.
- No patch-size, line-count, edit-tool, command-order, or failure requirement exists in the verifier.
- The workspace observer's expected/unexpected classification is descriptive and does not determine reward.
