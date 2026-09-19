from batchline.api.serializers.jobs import serialize_job, serialize_job_summary
from batchline.cli.render.jobs import render_job_detail
from batchline.jobs.models import Job
from batchline.jobs.service import JobService


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


# Direct model construction: the new value is retained, and omission remains valid.
direct = Job(id="job_direct", kind="thumbnail", queue="media", submitted_by="console/alice")
check(direct.submitted_by == "console/alice", "Job must retain submitted_by")

absent = Job(id="job_absent", kind="thumbnail", queue="media")
check(absent.submitted_by is None, "submitted_by must default to None")

# Mapping construction: present values survive and old mappings still load.
from_mapping = Job.from_mapping(
    {
        "id": "job_mapping",
        "kind": "transcode",
        "queue": "video",
        "submitted_by": "automation:nightly",
        "payload": {"asset_id": "asset_7"},
    }
)
check(from_mapping.submitted_by == "automation:nightly", "Job.from_mapping must preserve submitted_by")
check(from_mapping.payload == {"asset_id": "asset_7"}, "Job.from_mapping must preserve existing payload behavior")

legacy_mapping = Job.from_mapping({"id": "job_legacy", "kind": "index", "queue": "search"})
check(legacy_mapping.submitted_by is None, "legacy mappings without submitted_by must still load")

# Service submission: propagate both explicit and omitted values.
service = JobService()
submitted = service.submit(
    job_id="job_service",
    kind="thumbnail",
    queue="media",
    submitted_by="api-client-7",
    payload={"asset_id": "asset_42"},
)
check(submitted.submitted_by == "api-client-7", "JobService.submit must preserve submitted_by")
check(submitted.payload == {"asset_id": "asset_42"}, "JobService.submit must preserve existing payload behavior")

submitted_without = service.submit(job_id="job_service_legacy", kind="cleanup", queue="maintenance")
check(submitted_without.submitted_by is None, "JobService.submit must remain compatible when submitted_by is omitted")

# Full and summary API representations: always expose the key, using None when absent.
full = serialize_job(submitted)
check(full.get("submitted_by") == "api-client-7", "serialize_job must expose submitted_by")
check(full.get("status") == "queued", "serialize_job must preserve existing job fields")

summary = serialize_job_summary(submitted)
check(summary.get("submitted_by") == "api-client-7", "serialize_job_summary must expose submitted_by")
check(summary.get("status") == "queued", "serialize_job_summary must preserve existing job fields")

full_absent = serialize_job(submitted_without)
summary_absent = serialize_job_summary(submitted_without)
check("submitted_by" in full_absent and full_absent["submitted_by"] is None,
      "serialize_job must expose submitted_by=None when absent")
check("submitted_by" in summary_absent and summary_absent["submitted_by"] is None,
      "serialize_job_summary must expose submitted_by=None when absent")

# CLI detail output: visible label and the explicit absent-value form.
detail = render_job_detail(submitted)
check("Submitted by: api-client-7" in detail, "render_job_detail must show submitted_by")

absent_detail = render_job_detail(submitted_without)
check("Submitted by: -" in absent_detail, "render_job_detail must show '-' when submitted_by is absent")
