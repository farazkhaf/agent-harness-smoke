# Job policies

Batchline keeps per-kind operational defaults in `config/job-policies.toml`. The catalog is intended for values that differ by job kind but are stable enough to review in source control: queue ownership, worker pool, retry class, execution limits, rate-limit class, event emission, retention, and audit defaults.

The catalog is deliberately separate from deployment service configuration. Service configuration describes runtime services such as workers and APIs; job policies describe how individual kinds of work should be dispatched and retained.

Use `batchline.policies.load_job_policies()` to load and validate the catalog. Unknown or missing settings are rejected so accidental spelling drift cannot silently change policy behavior.
