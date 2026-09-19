from datetime import UTC, datetime

from batchline.operations import ArchiveRecord, iter_archive, matching_event_ids, write_archive


def test_archive_round_trip(tmp_path):
    path = tmp_path / "events.jsonl"
    write_archive(
        path,
        [
            ArchiveRecord(
                event_id="evt-2",
                occurred_at="2026-08-14T00:00:06Z",
                event_type="worker.rate_limited",
                worker="worker-03",
                service="thumbnailer",
                queue="media",
                provider="images-api",
            ),
            ArchiveRecord(
                event_id="evt-1",
                occurred_at="2026-08-14T00:00:03Z",
                event_type="worker.rate_limited",
                worker="worker-03",
                service="thumbnailer",
                queue="media",
                provider="images-api",
            ),
        ],
    )
    assert [record.event_id for record in iter_archive(path)] == ["evt-2", "evt-1"]
    assert matching_event_ids(
        path,
        worker="worker-03",
        event_type="worker.rate_limited",
        provider="images-api",
        start_at=datetime(2026, 8, 14, 0, 0, tzinfo=UTC),
    ) == ("evt-1", "evt-2")
