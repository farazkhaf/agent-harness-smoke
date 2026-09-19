from batchline.api.serializers.jobs import serialize_job, serialize_job_summary


def test_job_serializer_uses_canonical_status(queued_job):
    data = serialize_job(queued_job, include_payload=True)
    assert data["status"] == "queued"
    assert data["payload"] == {"asset_id": "asset_42"}


def test_summary_has_presentation_metadata(queued_job):
    data = serialize_job_summary(queued_job)
    assert data["status_label"] == "Queued"
    assert data["status_category"] == "waiting"
    assert data["terminal"] is False
