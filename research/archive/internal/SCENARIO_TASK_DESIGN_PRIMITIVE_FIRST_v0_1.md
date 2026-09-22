# Scenario Task Design — Primitive-First Authoring Note v0.1

Status: **internal task-designer guidance**. This is not a solver-facing document, verifier policy, or research result.

## 1. Design order

For this benchmark family, the interaction workload is the primary design requirement. Product realism is the wrapper that makes that workload coherent.

Use this order:

1. choose the repository-interaction primitives to compose;
2. set a target physical operation shape using the focused tasks as calibration;
3. prototype one or more repository patches that realize that shape;
4. only then choose/refine the product/maintenance story that makes the patch a legitimate engineering request;
5. write the solver-facing contract from the chosen software target;
6. build the oracle and verifier together;
7. run a diagnostic solver and confirm that the intended pressure actually appears before freeze.

Do not start from the most natural product feature and then accept whatever edit shape it happens to produce. If the product wrapper collapses a primary primitive into a materially smaller/easier operation, replace or reshape the wrapper.

Product coherence remains necessary, but it is a **guardrail**, not the optimization objective.

## 2. Calibration references

The focused tasks provide concrete operation magnitudes. These are authoring references, not universal thresholds and never verifier rules.

### B1 — coordinated multi-file modification

Matched OpenCode route:

- 4 source-code files changed;
- 6 coordinated `edit` mutations;
- model/service/serializer/CLI behavior had to remain synchronized.

Scenario implication: the B1-like component should still span several real source/product surfaces. A scenario should not reduce this to one central edit plus cosmetic propagation.

### R1 — selective repeated edit

Matched OpenCode route:

- one 542-line TOML catalog;
- 20 near-repeated job-policy sections;
- exactly 3 target sections changed;
- each mutation required enough surrounding section context to establish a safe anchor;
- the edit tool itself succeeded. Tool failure was not the pressure.

Scenario implication: if selective editing is claimed, the starting artifact should contain repeated/near-repeated structures with several intended targets and many protected non-targets. Small edits can be high-pressure when localization/anchoring is selective.

### R4 — substantial extraction/module split

Matched OpenCode route:

- starting source module about 572 lines;
- new module write about 10.6k characters / ~260 lines;
- old module lost a contiguous ~241-line implementation region while preserving unrelated code;
- import/reference integration remained required;
- OpenCode used a whole-file write for the destination, boundary inspection, and shell deletion for the large old-region removal.

Scenario implication: a claimed R4-like component must contain a materially substantial physical refactor. Merely moving a 50–100 line helper family and calling it an extraction is insufficient.

## 3. Scenario composition targets

Before product design, write an internal **pressure specification**. For each primary primitive, record:

- expected source/destination files;
- approximate existing code/data affected;
- contiguous versus dispersed regions;
- number of new/moved/deleted modules or artifacts;
- preservation/reference obligations;
- whether the workspace naturally admits multiple editing routes;
- focused baseline used for comparison.

For Scenario 1 RC2, the working target envelope is:

### Primary A — B1-like coordination

Aim for:

- at least 4 meaningful source-code files;
- roughly 6 or more coordinated source mutations;
- at least 3 real subsystem/surface boundaries (for example runtime state, public representation/commands, event machinery, schema/config);
- omissions on one surface should plausibly leave the software incomplete.

More files are not automatically better. Every changed surface must be justified by the final contract.

### Primary B — substantial refactor/extraction

Aim for an operation in approximately the same *physical class* as R4 without reproducing R4 verbatim:

- roughly 180–300 lines (or comparable 8–12k characters) of existing implementation physically relocated/reorganized, **or an equivalent multi-region/multi-destination transformation**;
- meaningful creation/move/removal work, not only new feature lines;
- enough preserved surrounding code or enough destination decomposition that the old state cannot be treated as a trivial tiny local replacement;
- imports/references/compatibility require reconciliation;
- the route may reasonably be expressed through structured edits, whole-file writes, shell/text operations, scripts, or another valid mechanism.

Do not require a tool to fail. A clean specialized route is a positive result. The authoring question is whether the operation gives the harness meaningful route choices.

### Optional C — R1-like selectivity

Include only if a coherent wrapper naturally supports it. A good instance would have:

- a large structured artifact (roughly 400+ lines);
- 10+ repeated/near-repeated records or blocks;
- 3+ specified non-adjacent target regions;
- strong preservation of non-target records;
- local context needed to identify safe edit anchors.

If this shape is absent, do not claim an R1 link merely because JSON/TOML/schema text was edited.

## 4. Context stewardship

Context stewardship is expected to emerge from **composition of substantive operations**, not from semantic ambiguity or irrelevant repository padding.

A scenario may naturally require the solver to retain:

- a large structural source region;
- several coordinated source surfaces;
- a large schema/config artifact;
- compatibility/import facts discovered earlier.

Do not add unrelated files or obscure product requirements merely to increase token use.

## 5. Product wrapper comes second

Once the pressure specification is satisfactory, choose the smallest coherent engineering story that makes those operations legitimate.

The product wrapper may name exact files/modules/maintenance structure when that is a realistic engineering requirement. Route freedom concerns **how the solver reaches the specified target**, not freedom to choose a different software architecture.

Reject a wrapper when:

- it makes the intended refactor too small;
- it allows a one-file shortcut that destroys the multi-file pressure;
- it creates semantic/reasoning difficulty instead of edit pressure;
- it requires unrelated feature breadth merely to inflate patch size;
- it reproduces a focused task almost exactly rather than composing its interaction class inside a different change.

## 6. Verifier boundary

The pressure specification is **never** a hidden verifier specification.

The verifier may check only requirements present in the solver-facing contract. Therefore:

- if a file/module name is structurally required, name it in the instruction;
- if an implementation must be absent from an old module, say so;
- if compatibility imports must remain, say so;
- do not check hidden keywords, source strings, AST shapes, file counts, line counts, tool use, or patch size unless that exact property is a legitimate explicit contract requirement.

Authoring measurements such as moved-line counts, repeated-region counts, or whether `replace_str` looks comfortable are used only to decide whether the task is a good instrument before freeze.

## 7. Tool failure is not the target

A successful `edit`, `write`, patch, shell command, or script says nothing by itself about task adequacy.

Study:

- why a route was chosen;
- what operation shape it was applied to;
- whether another harness exposes a different useful route;
- how much localization/context was required before the operation;
- whether large/dispersed operations were decomposed or handled directly.

Tool errors caused by quoting, escaping, malformed arguments, or accidental anchors are incidental diagnostics unless the task was explicitly designed around recovery.
