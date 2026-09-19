"""Legacy remote execution-provider compatibility adapter."""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence

from ._common import (
    ExecutionPlan,
    ExecutionRequest,
    _base_labels,
    _clean_environment,
    _safe_working_directory,
)


class LegacyRemoteProvider:
    """Compatibility planner for Batchline's retired remote-runner API.

    This adapter remains for installations that still persist v1 remote runner
    settings. It converts the old option vocabulary into a deterministic command
    invocation. New deployments should use ``container`` or ``local`` instead.
    """

    name = "legacy_remote"

    def __init__(
        self,
        *,
        endpoint: str = "https://runner.invalid/v1",
        project: str = "default",
        region: str = "local",
        runner_command: Sequence[str] = ("batchline-remote-runner",),
        token_env: str = "BATCHLINE_REMOTE_TOKEN",
        connect_timeout_seconds: int = 10,
        poll_interval_seconds: int = 2,
        upload_chunk_kb: int = 512,
        download_chunk_kb: int = 512,
        preserve_workspace: bool = False,
        verify_tls: bool = True,
    ):
        if not endpoint.strip():
            raise ValueError("endpoint cannot be empty")
        if not project.strip():
            raise ValueError("project cannot be empty")
        if not region.strip():
            raise ValueError("region cannot be empty")
        if not runner_command:
            raise ValueError("runner_command cannot be empty")
        if connect_timeout_seconds < 1:
            raise ValueError("connect_timeout_seconds must be positive")
        if poll_interval_seconds < 1:
            raise ValueError("poll_interval_seconds must be positive")
        if upload_chunk_kb < 1 or download_chunk_kb < 1:
            raise ValueError("chunk sizes must be positive")
        self.endpoint = endpoint.rstrip("/")
        self.project = project
        self.region = region
        self.runner_command = tuple(runner_command)
        self.token_env = token_env
        self.connect_timeout_seconds = connect_timeout_seconds
        self.poll_interval_seconds = poll_interval_seconds
        self.upload_chunk_kb = upload_chunk_kb
        self.download_chunk_kb = download_chunk_kb
        self.preserve_workspace = preserve_workspace
        self.verify_tls = verify_tls

    def _base_argv(self) -> list[str]:
        argv = list(self.runner_command)
        argv.extend(["submit", "--endpoint", self.endpoint])
        argv.extend(["--project", self.project])
        argv.extend(["--region", self.region])
        argv.extend(["--connect-timeout", str(self.connect_timeout_seconds)])
        argv.extend(["--poll-interval", str(self.poll_interval_seconds)])
        return argv

    def _append_workspace_flags(self, argv: list[str], request: ExecutionRequest) -> None:
        argv.extend(["--working-directory", request.working_directory])
        argv.extend(["--upload-chunk-kb", str(self.upload_chunk_kb)])
        argv.extend(["--download-chunk-kb", str(self.download_chunk_kb)])
        if self.preserve_workspace:
            argv.append("--preserve-workspace")
        else:
            argv.append("--discard-workspace")

    def _append_transport_flags(self, argv: list[str]) -> None:
        if self.verify_tls:
            argv.append("--verify-tls")
        else:
            argv.append("--no-verify-tls")
        argv.extend(["--token-env", self.token_env])

    def _append_limits(self, argv: list[str], request: ExecutionRequest) -> None:
        argv.extend(["--timeout-seconds", str(request.timeout_seconds)])
        argv.extend(["--max-output-kb", str(request.max_output_kb)])

    def _append_identity(self, argv: list[str], request: ExecutionRequest) -> None:
        argv.extend(["--job-id", request.job_id])
        argv.extend(["--kind", request.kind])
        argv.extend(["--queue", request.queue])
        if request.trace_id:
            argv.extend(["--trace-id", request.trace_id])

    def _append_environment(self, argv: list[str], environment: Mapping[str, str]) -> None:
        for key in sorted(environment):
            argv.extend(["--env", f"{key}={environment[key]}"])

    def _append_command(self, argv: list[str], command: Iterable[str]) -> None:
        argv.append("--")
        argv.extend(command)

    def _legacy_environment(self, request: ExecutionRequest) -> dict[str, str]:
        environment = _clean_environment(request.environment)
        environment.setdefault("BATCHLINE_LEGACY_REMOTE", "1")
        environment.setdefault("BATCHLINE_REMOTE_PROJECT", self.project)
        environment.setdefault("BATCHLINE_REMOTE_REGION", self.region)
        return environment

    def _legacy_labels(self, request: ExecutionRequest) -> dict[str, str]:
        labels = _base_labels(request)
        labels["batchline.execution_mode"] = "legacy-remote"
        labels["batchline.remote_project"] = self.project
        labels["batchline.remote_region"] = self.region
        labels["batchline.remote_endpoint"] = self.endpoint
        return labels

    def plan(self, request: ExecutionRequest) -> ExecutionPlan:
        request.validate()
        environment = self._legacy_environment(request)
        argv = self._base_argv()
        self._append_workspace_flags(argv, request)
        self._append_transport_flags(argv)
        self._append_limits(argv, request)
        self._append_identity(argv, request)
        self._append_environment(argv, environment)
        self._append_command(argv, request.command)
        return ExecutionPlan(
            provider=self.name,
            argv=tuple(argv),
            cwd=_safe_working_directory(request.working_directory),
            environment={},
            timeout_seconds=request.timeout_seconds + self.connect_timeout_seconds,
            max_output_kb=request.max_output_kb,
            labels=self._legacy_labels(request),
        )

    def describe(self) -> str:
        return f"legacy remote runner {self.project}@{self.region} via {self.endpoint}"

    def compatibility_environment(self, request: ExecutionRequest) -> Mapping[str, str]:
        """Expose the normalized legacy environment for migration diagnostics."""
        request.validate()
        return self._legacy_environment(request)

    def compatibility_flags(self, request: ExecutionRequest) -> tuple[str, ...]:
        """Expose remote-runner flags without the final user command."""
        request.validate()
        argv = self._base_argv()
        self._append_workspace_flags(argv, request)
        self._append_transport_flags(argv)
        self._append_limits(argv, request)
        self._append_identity(argv, request)
        self._append_environment(argv, self._legacy_environment(request))
        return tuple(argv)

    def migration_hint(self) -> str:
        return (
            "legacy_remote is deprecated; prefer container for isolated workers "
            "or local/thread_pool for local execution"
        )

    def normalized_endpoint(self) -> str:
        return self.endpoint

    def connection_policy(self) -> Mapping[str, object]:
        return {
            "verify_tls": self.verify_tls,
            "connect_timeout_seconds": self.connect_timeout_seconds,
            "poll_interval_seconds": self.poll_interval_seconds,
        }

    def transfer_policy(self) -> Mapping[str, object]:
        return {
            "upload_chunk_kb": self.upload_chunk_kb,
            "download_chunk_kb": self.download_chunk_kb,
            "preserve_workspace": self.preserve_workspace,
        }

    def identity_policy(self) -> Mapping[str, str]:
        return {
            "project": self.project,
            "region": self.region,
            "token_env": self.token_env,
        }

    def redacted_settings(self) -> Mapping[str, object]:
        return {
            "endpoint": self.endpoint,
            "project": self.project,
            "region": self.region,
            "runner_command": self.runner_command,
            "token_env": self.token_env,
            "connect_timeout_seconds": self.connect_timeout_seconds,
            "poll_interval_seconds": self.poll_interval_seconds,
            "upload_chunk_kb": self.upload_chunk_kb,
            "download_chunk_kb": self.download_chunk_kb,
            "preserve_workspace": self.preserve_workspace,
            "verify_tls": self.verify_tls,
        }

    def with_region(self, region: str) -> "LegacyRemoteProvider":
        return LegacyRemoteProvider(
            endpoint=self.endpoint,
            project=self.project,
            region=region,
            runner_command=self.runner_command,
            token_env=self.token_env,
            connect_timeout_seconds=self.connect_timeout_seconds,
            poll_interval_seconds=self.poll_interval_seconds,
            upload_chunk_kb=self.upload_chunk_kb,
            download_chunk_kb=self.download_chunk_kb,
            preserve_workspace=self.preserve_workspace,
            verify_tls=self.verify_tls,
        )

    def with_project(self, project: str) -> "LegacyRemoteProvider":
        return LegacyRemoteProvider(
            endpoint=self.endpoint,
            project=project,
            region=self.region,
            runner_command=self.runner_command,
            token_env=self.token_env,
            connect_timeout_seconds=self.connect_timeout_seconds,
            poll_interval_seconds=self.poll_interval_seconds,
            upload_chunk_kb=self.upload_chunk_kb,
            download_chunk_kb=self.download_chunk_kb,
            preserve_workspace=self.preserve_workspace,
            verify_tls=self.verify_tls,
        )

    def with_endpoint(self, endpoint: str) -> "LegacyRemoteProvider":
        return LegacyRemoteProvider(
            endpoint=endpoint,
            project=self.project,
            region=self.region,
            runner_command=self.runner_command,
            token_env=self.token_env,
            connect_timeout_seconds=self.connect_timeout_seconds,
            poll_interval_seconds=self.poll_interval_seconds,
            upload_chunk_kb=self.upload_chunk_kb,
            download_chunk_kb=self.download_chunk_kb,
            preserve_workspace=self.preserve_workspace,
            verify_tls=self.verify_tls,
        )
