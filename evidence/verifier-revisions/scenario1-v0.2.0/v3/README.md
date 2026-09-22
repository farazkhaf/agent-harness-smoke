# Scenario 1 verifier r3

Revision `r3` is the current verifier for Scenario 1 task version `0.2.0`.

It accepts equivalent schema-reference layouts when concrete worker schema ownership resides in `worker-events.schema.json`, while continuing to reject concrete worker definitions retained in the aggregate schema. It also checks the drain/resume preservation fields stated by the task without requiring Python object identity.

Regression controls in this directory cover the author solution, a direct external `$ref` with a harmless `type: object` sibling, a renamed concrete worker definition, and an altered registry return.
