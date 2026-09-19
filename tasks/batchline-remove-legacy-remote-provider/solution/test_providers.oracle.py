import pytest

from batchline.execution import ExecutionRequest, get_provider, provider_names


def _request():
    return ExecutionRequest(
        job_id="job-123",
        kind="thumbnail",
        queue="media",
        command=("python", "worker.py"),
        environment={"MODE": "test"},
        trace_id="trace-9",
    )


def test_current_provider_plans_are_available():
    assert {"local", "thread_pool", "container", "sandbox", "batch_file", "container_pool"}.issubset(provider_names())
    local = get_provider("local").plan(_request())
    assert local.argv == ("python", "worker.py")
    assert local.labels["batchline.job_id"] == "job-123"


def test_container_provider_builds_deterministic_command():
    plan = get_provider("container").plan(_request())
    assert plan.argv[:3] == ("docker", "run", "--rm")
    assert "batchline-worker:stable" in plan.argv
    assert plan.argv[-2:] == ("python", "worker.py")



def test_unknown_provider_is_rejected():
    with pytest.raises(KeyError):
        get_provider("missing")
