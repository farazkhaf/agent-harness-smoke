# Retain job submitter metadata

Batchline needs to retain who submitted a job.

Add an optional `submitted_by` field to jobs.

- `JobService.submit()` must accept an optional `submitted_by` value and retain it on the created job.
- `Job.from_mapping()` must preserve `submitted_by` when it is present.
- `serialize_job()` and `serialize_job_summary()` must both include a `submitted_by` key. Use the submitted string when present and `None` when it is absent.
- `render_job_detail()` must include `Submitted by: <value>` when present and `Submitted by: -` when it is absent.

Existing jobs and calls that do not provide `submitted_by` must continue to work.
