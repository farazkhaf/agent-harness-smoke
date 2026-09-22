# Scenario 1 RC2 — Primitive-First Design Direction v0.2

Status: **internal pre-contract design direction**. This supersedes the earlier RC2 direction that prematurely locked a product-domain event split.

## 1. Why RC2 is being redesigned

RC1 was solvable and verifier-correct, but the OpenCode diagnostic showed two authoring defects:

1. the main structural extraction was physically weaker than the matched R4 baseline;
2. optional solver-authored tests became a larger source of route variance than the intended editing spine.

RC2 therefore starts from the required interaction workload, not from an already-fixed product architecture.

## 2. Primary workload for RC2

### A. Coordinated multi-file source work — required

Retain a B1-like component at or above the focused-task level:

- 4+ meaningful source-code files;
- roughly 6+ coordinated source mutations;
- multiple subsystem boundaries;
- final correctness requires synchronization across those surfaces.

The existing worker drain/resume lifecycle is still a plausible wrapper for this component because it naturally touches model/state, registry/capacity, public representation/commands, and event behavior.

### B. Substantial refactor/extraction — required

RC2 must add a structural operation with a physical workload comparable to the **class** calibrated by R4, but not copy R4's exact provider-class extraction.

Authoring target:

- roughly 180–300 lines / 8–12k characters of existing implementation reorganized or an equivalent multi-region/multi-destination transformation;
- at least one material create/move/delete/module-split operation;
- preservation of unrelated implementation or enough destination decomposition that the transformation cannot be reduced to a few tiny local replacements;
- import/reference/compatibility reconciliation;
- no required edit tool or failure mode.

A candidate fails this criterion if the source can simply be rewritten to a tiny facade and all difficult preservation disappears, unless the destination decomposition itself provides equivalent structural pressure.

### C. Selective coordinated editing — desirable, not mandatory

If the product wrapper can naturally require it, add an R1-like selective component:

- a large repeated structured artifact;
- several named target regions among many similar non-target regions;
- preservation of all non-targets;
- safe localization/anchoring matters more than edit size.

Do not bolt this on if it produces an artificial product requirement. If absent, RC2 will not make an R1 focused-link claim.

### D. Context stewardship — emergent

The scenario should require the solver to carry information across the substantial refactor and the distributed feature edits. Context pressure should come from the amount and distribution of relevant repository state, not from ambiguous instructions.

## 3. RC1 and the earlier RC2 domain-split candidate

### RC1 worker-only event extraction

Rejected as underpowered for the structural primitive:

- new worker module ~146 lines in the OpenCode route;
- old encoder removal ~97 lines;
- the removal remained comfortable as one normal string replacement.

### Earlier RC2 idea: split all event constructors by domain and make `encoder.py` a facade

Keep only as a **candidate shape**, not a settled target.

It improves aggregate moved code (~200 lines), but it has a possible weakness: because the starting encoder is only ~228 lines, a solver may replace the entire file with a small compatibility facade rather than perform a preservation-sensitive extraction. That may still be a valid substantial multi-destination refactor, but it must be measured in an oracle/shape probe before acceptance.

Do not choose it merely because it is product-coherent.

## 4. Next design step: patch-shape probes before contract prose

Before writing RC2 solver instructions, prototype 2–3 structural wrappers and record for each:

| Property | Record |
|---|---|
| Existing implementation physically moved/reorganized | lines/chars and source regions |
| Old-location preservation burden | what unrelated code remains |
| New modules/files | count and approximate sizes |
| Reference/import migration | affected call/import surfaces |
| Selective large-artifact edits | target regions vs repeated non-targets |
| Coordinated feature surfaces | source files/subsystems |
| Trivial whole-file/local-replace shortcut | yes/no and why |
| Product rationale | one short engineering explanation |

Choose the wrapper that best satisfies the pressure targets with the least semantic ambiguity.

The product rationale is allowed to be simple. It only needs to make the requested maintenance change believable and internally coherent.

## 5. Scope rule retained from RC1 diagnostic

Unless a later pressure specification explicitly makes tests or docs part of the target:

> Leave existing files under `tests/` and `docs/` unchanged. Use the repository's existing tests and validation commands to validate the change.

This bounds irrelevant route variance. It does not prescribe command order or prohibit temporary/non-final reasoning aids outside the repository contract.

## 6. Solver-contract and verifier rule once the wrapper is chosen

The eventual instruction should be explicit about the desired software structure. If a specific module split, file name, compatibility surface, or absence requirement is important, state it directly.

The verifier may then check that explicit structure narrowly.

The verifier must **not** check the internal authoring pressure targets:

- no line-count thresholds;
- no required tool use;
- no patch-size checks;
- no hidden source keywords or file names;
- no preferred helper layout unless the solver instruction explicitly requires it.

## 7. RC2 clearance question

The next diagnostic run should answer:

> Did the chosen RC2 wrapper preserve B1-like coordination and create a genuinely substantial structural editing operation, with route/context pressure concentrated there rather than in optional testing or semantic ambiguity?

Only after that answer is yes should Scenario 1 freeze.
