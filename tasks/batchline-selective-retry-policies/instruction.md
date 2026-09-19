# Update retry policies for selected job kinds

Batchline needs more aggressive retry handling for three existing job kinds.

In the job policy catalog, change `retry_policy` to `aggressive` for exactly these job kinds:

- `thumbnail`
- `billing_export`
- `daily_digest`

Leave every other job policy setting unchanged. All other job kinds must keep their existing retry policy.

The policy catalog must continue to load and validate normally.
