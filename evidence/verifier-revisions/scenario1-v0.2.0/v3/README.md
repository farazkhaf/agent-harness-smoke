# Verifier revision 3

Revision 3 preserves the r2 contract correction and adds two regression guards derived from the same behavior/explicit-structure verifier philosophy.

- A concrete worker event definition remaining in aggregate `$defs` fails even if the definition is renamed.
- Registry drain/resume returned and stored snapshots must preserve the fields explicitly named in the task contract.
- A direct external worker `$ref` may carry a harmless sibling such as `"type": "object"`; r3 does not require a bare-reference canonical form.

No recorded Scenario 1 workspace uses either newly guarded edge case, so recorded r2 outcomes remain unchanged. No agent run was repeated for r3.

Included regression artifacts:

- `oracle-verifier.json` — author solution passes G1-G6.
- `direct-external-ref-with-type.json` — passes.
- `renamed-concrete-definition.json` — G5 fails.
- `altered-registry-return.json` — G1/G2 fail because physical capacity is not preserved.
