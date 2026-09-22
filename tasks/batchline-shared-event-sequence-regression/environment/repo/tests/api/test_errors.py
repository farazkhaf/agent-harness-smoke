import pytest

from batchline.api.errors import error_payload


def test_error_payload_is_stable():
    assert error_payload("job_not_found", "Job does not exist", detail={"job_id": "missing"}) == {
        "error": {
            "code": "job_not_found",
            "message": "Job does not exist",
            "detail": {"job_id": "missing"},
        }
    }


def test_error_payload_rejects_empty_code():
    with pytest.raises(ValueError, match="error code"):
        error_payload("", "message")
