"""Execution-provider planning.

Batchline does not launch external infrastructure itself. Providers translate a
job execution request into a deterministic local execution plan that a caller
can inspect or execute. The module still carries the older ``legacy_remote``
compatibility implementation inline while the execution package is being split
into smaller provider modules.
"""

from __future__ import annotations

from typing import Sequence

from ._common import (
    ExecutionPlan,
    ExecutionProvider,
    ExecutionRequest,
    _base_labels,
    _clean_environment,
    _safe_working_directory,
)
from .legacy_remote import LegacyRemoteProvider


class LocalProcessProvider:
    """Plan direct local process execution."""

    name = "local"

    def __init__(self, *, python_unbuffered: bool = True, inherit_path: bool = True):
        self.python_unbuffered = python_unbuffered
        self.inherit_path = inherit_path

    def plan(self, request: ExecutionRequest) -> ExecutionPlan:
        request.validate()
        environment = _clean_environment(request.environment)
        if self.python_unbuffered:
            environment.setdefault("PYTHONUNBUFFERED", "1")
        if not self.inherit_path:
            environment.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin")
        labels = _base_labels(request)
        labels["batchline.execution_mode"] = "local-process"
        return ExecutionPlan(
            provider=self.name,
            argv=tuple(request.command),
            cwd=_safe_working_directory(request.working_directory),
            environment=environment,
            timeout_seconds=request.timeout_seconds,
            max_output_kb=request.max_output_kb,
            labels=labels,
        )

    def describe(self) -> str:
        return "direct local process execution"


class ThreadPoolProvider:
    """Plan a local command for execution by a shared worker pool."""

    name = "thread_pool"

    def __init__(self, *, pool_name: str = "default", concurrency: int = 4):
        if not pool_name.strip():
            raise ValueError("pool_name cannot be empty")
        if concurrency < 1:
            raise ValueError("concurrency must be positive")
        self.pool_name = pool_name
        self.concurrency = concurrency

    def plan(self, request: ExecutionRequest) -> ExecutionPlan:
        request.validate()
        environment = _clean_environment(request.environment)
        environment["BATCHLINE_POOL"] = self.pool_name
        environment["BATCHLINE_POOL_CONCURRENCY"] = str(self.concurrency)
        labels = _base_labels(request)
        labels["batchline.execution_mode"] = "thread-pool"
        labels["batchline.pool"] = self.pool_name
        return ExecutionPlan(
            provider=self.name,
            argv=tuple(request.command),
            cwd=_safe_working_directory(request.working_directory),
            environment=environment,
            timeout_seconds=request.timeout_seconds,
            max_output_kb=request.max_output_kb,
            labels=labels,
        )

    def describe(self) -> str:
        return f"shared local pool {self.pool_name} ({self.concurrency} workers)"


class ContainerCommandProvider:
    """Plan a deterministic container CLI invocation.

    The provider emits a command plan only; it does not require Docker or another
    container runtime to be installed in the task environment.
    """

    name = "container"

    def __init__(
        self,
        *,
        image: str = "batchline-worker:stable",
        runtime_command: Sequence[str] = ("docker", "run", "--rm"),
        network: str = "none",
        read_only: bool = True,
    ):
        if not image.strip():
            raise ValueError("image cannot be empty")
        if not runtime_command:
            raise ValueError("runtime_command cannot be empty")
        self.image = image
        self.runtime_command = tuple(runtime_command)
        self.network = network
        self.read_only = read_only

    def plan(self, request: ExecutionRequest) -> ExecutionPlan:
        request.validate()
        environment = _clean_environment(request.environment)
        argv: list[str] = list(self.runtime_command)
        argv.extend(["--network", self.network])
        if self.read_only:
            argv.append("--read-only")
        argv.extend(["--workdir", request.working_directory])
        for key in sorted(environment):
            argv.extend(["--env", f"{key}={environment[key]}"])
        labels = _base_labels(request)
        for key in sorted(labels):
            argv.extend(["--label", f"{key}={labels[key]}"])
        argv.append(self.image)
        argv.extend(request.command)
        labels["batchline.execution_mode"] = "container-command"
        labels["batchline.image"] = self.image
        return ExecutionPlan(
            provider=self.name,
            argv=tuple(argv),
            cwd=_safe_working_directory(request.working_directory),
            environment={},
            timeout_seconds=request.timeout_seconds,
            max_output_kb=request.max_output_kb,
            labels=labels,
        )

    def describe(self) -> str:
        return f"container command using {self.image}"


class SandboxProcessProvider:
    """Plan a local process with a constrained environment and resource labels."""

    name = "sandbox"

    def __init__(
        self,
        *,
        sandbox_root: str = "/tmp/batchline-sandboxes",
        profile: str = "default",
        network_access: bool = False,
        writable_tmp: bool = True,
    ):
        if not sandbox_root.startswith("/"):
            raise ValueError("sandbox_root must be absolute")
        if not profile.strip():
            raise ValueError("profile cannot be empty")
        self.sandbox_root = sandbox_root.rstrip("/")
        self.profile = profile
        self.network_access = network_access
        self.writable_tmp = writable_tmp

    def sandbox_directory(self, request: ExecutionRequest) -> str:
        request.validate()
        return f"{self.sandbox_root}/{request.job_id}"

    def plan(self, request: ExecutionRequest) -> ExecutionPlan:
        request.validate()
        environment = _clean_environment(request.environment)
        environment["BATCHLINE_SANDBOX_PROFILE"] = self.profile
        environment["BATCHLINE_SANDBOX_ROOT"] = self.sandbox_directory(request)
        environment["BATCHLINE_NETWORK_ACCESS"] = "1" if self.network_access else "0"
        environment["BATCHLINE_WRITABLE_TMP"] = "1" if self.writable_tmp else "0"
        labels = _base_labels(request)
        labels["batchline.execution_mode"] = "sandbox-process"
        labels["batchline.sandbox_profile"] = self.profile
        labels["batchline.network_access"] = "enabled" if self.network_access else "disabled"
        return ExecutionPlan(
            provider=self.name,
            argv=tuple(request.command),
            cwd=_safe_working_directory(request.working_directory),
            environment=environment,
            timeout_seconds=request.timeout_seconds,
            max_output_kb=request.max_output_kb,
            labels=labels,
        )

    def describe(self) -> str:
        network = "networked" if self.network_access else "offline"
        return f"{network} sandbox profile {self.profile}"


class BatchFileProvider:
    """Plan execution through a local batch command-file runner."""

    name = "batch_file"

    def __init__(
        self,
        *,
        runner_command: Sequence[str] = ("batchline-batch-runner",),
        spool_directory: str = "/var/tmp/batchline-spool",
        retain_command_file: bool = False,
    ):
        if not runner_command:
            raise ValueError("runner_command cannot be empty")
        if not spool_directory.startswith("/"):
            raise ValueError("spool_directory must be absolute")
        self.runner_command = tuple(runner_command)
        self.spool_directory = spool_directory.rstrip("/")
        self.retain_command_file = retain_command_file

    def command_file(self, request: ExecutionRequest) -> str:
        request.validate()
        return f"{self.spool_directory}/{request.job_id}.cmd"

    def plan(self, request: ExecutionRequest) -> ExecutionPlan:
        request.validate()
        environment = _clean_environment(request.environment)
        command_file = self.command_file(request)
        argv = list(self.runner_command)
        argv.extend(["--command-file", command_file])
        argv.extend(["--cwd", request.working_directory])
        argv.extend(["--timeout", str(request.timeout_seconds)])
        argv.extend(["--max-output-kb", str(request.max_output_kb)])
        if self.retain_command_file:
            argv.append("--retain-command-file")
        else:
            argv.append("--delete-command-file")
        for key in sorted(environment):
            argv.extend(["--env", f"{key}={environment[key]}"])
        argv.append("--")
        argv.extend(request.command)
        labels = _base_labels(request)
        labels["batchline.execution_mode"] = "batch-file"
        labels["batchline.command_file"] = command_file
        return ExecutionPlan(
            provider=self.name,
            argv=tuple(argv),
            cwd=_safe_working_directory(request.working_directory),
            environment={},
            timeout_seconds=request.timeout_seconds,
            max_output_kb=request.max_output_kb,
            labels=labels,
        )

    def describe(self) -> str:
        return f"local batch command-file runner in {self.spool_directory}"


class ContainerPoolProvider:
    """Plan a command for a named pre-warmed container worker pool."""

    name = "container_pool"

    def __init__(
        self,
        *,
        pool: str = "default",
        dispatcher_command: Sequence[str] = ("batchline-container-dispatch",),
        isolation: str = "job",
    ):
        if not pool.strip():
            raise ValueError("pool cannot be empty")
        if not dispatcher_command:
            raise ValueError("dispatcher_command cannot be empty")
        if isolation not in {"job", "queue"}:
            raise ValueError("isolation must be job or queue")
        self.pool = pool
        self.dispatcher_command = tuple(dispatcher_command)
        self.isolation = isolation

    def plan(self, request: ExecutionRequest) -> ExecutionPlan:
        request.validate()
        environment = _clean_environment(request.environment)
        argv = list(self.dispatcher_command)
        argv.extend(["--pool", self.pool])
        argv.extend(["--isolation", self.isolation])
        argv.extend(["--job-id", request.job_id])
        argv.extend(["--queue", request.queue])
        argv.extend(["--timeout", str(request.timeout_seconds)])
        for key in sorted(environment):
            argv.extend(["--env", f"{key}={environment[key]}"])
        argv.append("--")
        argv.extend(request.command)
        labels = _base_labels(request)
        labels["batchline.execution_mode"] = "container-pool"
        labels["batchline.container_pool"] = self.pool
        labels["batchline.pool_isolation"] = self.isolation
        return ExecutionPlan(
            provider=self.name,
            argv=tuple(argv),
            cwd=_safe_working_directory(request.working_directory),
            environment={},
            timeout_seconds=request.timeout_seconds,
            max_output_kb=request.max_output_kb,
            labels=labels,
        )

    def describe(self) -> str:
        return f"pre-warmed container pool {self.pool} ({self.isolation} isolation)"


_PROVIDER_FACTORIES = {
    "local": LocalProcessProvider,
    "thread_pool": ThreadPoolProvider,
    "container": ContainerCommandProvider,
    "sandbox": SandboxProcessProvider,
    "batch_file": BatchFileProvider,
    "container_pool": ContainerPoolProvider,
    "legacy_remote": LegacyRemoteProvider,
}


def provider_names() -> tuple[str, ...]:
    return tuple(sorted(_PROVIDER_FACTORIES))


def get_provider(name: str) -> ExecutionProvider:
    try:
        factory = _PROVIDER_FACTORIES[name]
    except KeyError as exc:
        raise KeyError(f"unknown execution provider: {name}") from exc
    return factory()
