# Restore the shared lifecycle-event ID sequence

Batchline lifecycle event IDs are intended to draw from one process-wide monotonic sequence, regardless of event family. A recent change made the counters independent by event-ID prefix, so job, worker, retry, and service/config events can reuse the same numeric sequence value inside one Python process.

Fix the regression in `src/batchline/events/encoder.py` so all existing lifecycle-event constructors once again share one process-wide counter. Preserve the existing public constructor imports, event-ID prefixes, payload behavior, timestamps, and schema behavior.

Add exactly one regression test at:

`tests/events/test_event_sequence.py`

The test function must be named:

`test_event_id_sequence_is_shared_across_families`

The regression test must construct events from the job, worker, and service/config families in one Python process, include a later event after crossing families, and verify that the numeric sequence components increase monotonically by one across those events. The test must not assume that the first sequence value is `1` or any other fixed value.

Keep the task scoped to these two paths only:

- `src/batchline/events/encoder.py`
- `tests/events/test_event_sequence.py`

Do not add other tests or documentation. Existing repository tests and validation behavior must remain healthy.
