"""Thin Harbor wrapper for a preinstalled Mini-SWE-Agent runtime.

The stock Harbor MiniSweAgent installs Mini-SWE-Agent into every fresh task
container.  Harness Smoke runtime images already contain a pinned copy, so this
wrapper preserves Harbor's stock run/model/trajectory behavior and changes only
``install()``: setup becomes a strict version/executable check.

This module intentionally subclasses Harbor's built-in integration rather than
reimplementing Mini-SWE invocation or trajectory parsing.
"""

from __future__ import annotations

from typing import Any, override

from harbor.agents.installed.mini_swe_agent import MiniSweAgent
from harbor.environments.base import BaseEnvironment


class PreinstalledMiniSweAgent(MiniSweAgent):
    """Mini-SWE-Agent integration backed by a version-pinned runtime image."""

    DEFAULT_EXPECTED_VERSION = "2.4.6"
    RUNTIME_PROFILE_ID = "mini-swe-2.4.6"

    def __init__(
        self,
        *args: Any,
        version: str | None = None,
        **kwargs: Any,
    ) -> None:
        # Pin the version in Harbor's normal agent metadata as well as in the
        # runtime verification below.  Callers can deliberately override it
        # when validating a new image/version.
        super().__init__(
            *args,
            version=version or self.DEFAULT_EXPECTED_VERSION,
            **kwargs,
        )

    @override
    async def install(self, environment: BaseEnvironment) -> None:
        """Verify the pinned runtime instead of installing the agent again."""

        expected = self._version or self.DEFAULT_EXPECTED_VERSION

        # UV_TOOL_DIR is set in the runtime image.  `uv tool list` is the same
        # version-discovery mechanism used by Harbor's stock MiniSweAgent.
        result = await self.exec_as_agent(
            environment,
            command=(
                "set -euo pipefail; "
                "command -v mini-swe-agent >/dev/null; "
                "command -v uv >/dev/null; "
                "uv tool list 2>/dev/null | grep '^mini-swe-agent '"
            ),
        )
        installed = self.parse_version(result.stdout)

        if installed != expected:
            raise RuntimeError(
                "Preinstalled Mini-SWE-Agent version mismatch: "
                f"expected {expected!r}, found {installed!r}. "
                "Rebuild/select the matching Harness Smoke runtime image."
            )

        # Cheap executable smoke check.  No package manager/network call occurs.
        await self.exec_as_agent(
            environment,
            command="mini-swe-agent --help >/dev/null",
        )
