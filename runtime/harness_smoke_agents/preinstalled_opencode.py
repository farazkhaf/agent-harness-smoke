"""Thin Harbor wrapper for a preinstalled OpenCode runtime.

The stock Harbor OpenCode integration installs NVM, Node, and OpenCode into
fresh task containers. Harness Smoke runtime images already contain a pinned
copy, so this wrapper preserves Harbor's stock OpenCode run/config/trajectory
behavior and replaces only installation with strict runtime verification.

One compatibility detail is explicit here: OpenCode/models.dev names Fireworks
as ``fireworks-ai`` and reads ``FIREWORKS_API_KEY``. Harbor's model-connection
registry names the same provider ``fireworks_ai``. MODEL_CONNECTION therefore
resolves either common Fireworks key name while leaving the model string itself
in OpenCode's native ``fireworks-ai/...`` form.
"""

from __future__ import annotations

from typing import Any, override

from harbor.agents.installed.opencode import OpenCode
from harbor.agents.model_connection import ModelConnectionSpec
from harbor.environments.base import BaseEnvironment


class PreinstalledOpenCode(OpenCode):
    """OpenCode integration backed by a version-pinned runtime image."""

    DEFAULT_EXPECTED_VERSION = "1.18.30"
    RUNTIME_PROFILE_ID = "opencode-1.18.30"

    # Keep OpenCode's native provider/model identity (e.g. fireworks-ai/...),
    # but resolve Fireworks credentials through Harbor's existing
    # fireworks_ai provider entry. Accept either host-side key spelling and
    # canonicalize it to FIREWORKS_API_KEY for OpenCode.
    MODEL_CONNECTION = ModelConnectionSpec(
        default_provider="fireworks_ai",
        api_key_envs=("FIREWORKS_API_KEY", "FIREWORKS_AI_API_KEY"),
        passthrough=True,
    )

    def __init__(
        self,
        *args: Any,
        version: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            *args,
            version=version or self.DEFAULT_EXPECTED_VERSION,
            **kwargs,
        )

    @override
    async def install(self, environment: BaseEnvironment) -> None:
        """Verify the pinned NVM/Node/OpenCode runtime; perform no install."""

        expected = self._version or self.DEFAULT_EXPECTED_VERSION

        result = await self.exec_as_agent(
            environment,
            command=(
                "set -euo pipefail; "
                "test -s \"$HOME/.nvm/nvm.sh\"; "
                ". \"$HOME/.nvm/nvm.sh\"; "
                "command -v node >/dev/null; "
                "command -v npm >/dev/null; "
                "command -v opencode >/dev/null; "
                "opencode --version"
            ),
        )
        installed = result.stdout.strip().splitlines()[-1].strip() if result.stdout else ""

        if installed != expected:
            raise RuntimeError(
                "Preinstalled OpenCode version mismatch: "
                f"expected {expected!r}, found {installed!r}. "
                "Rebuild/select the matching Harness Smoke runtime image."
            )

        # The stock run() pipes JSONL through stdbuf; verify that dependency too.
        await self.exec_as_agent(
            environment,
            command=(
                "set -euo pipefail; "
                ". \"$HOME/.nvm/nvm.sh\"; "
                "command -v stdbuf >/dev/null; "
                "opencode --help >/dev/null"
            ),
        )
