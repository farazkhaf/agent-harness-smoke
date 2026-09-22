from batchline.cli.render.jobs import render_job_detail, render_job_row, render_job_table


def test_job_row_contains_status_and_queue(queued_job):
    row = render_job_row(queued_job)
    assert "Queued" in row
    assert "media" in row


def test_job_detail_has_named_fields(queued_job):
    detail = render_job_detail(queued_job)
    assert "Job: job_123" in detail
    assert "Status: Queued" in detail


def test_table_has_header(queued_job):
    table = render_job_table([queued_job])
    assert "STATUS" in table
    assert "thumbnail" in table
