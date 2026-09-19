# Remove the legacy remote execution provider

Batchline no longer supports the deprecated `legacy_remote` execution provider.

Remove the `LegacyRemoteProvider` implementation from `src/batchline/execution/providers.py`, remove `legacy_remote` from that module's provider registry, and remove the stale test coverage that exists only for that legacy provider.

After the change:

- `provider_names()` must no longer include `legacy_remote`.
- `get_provider("legacy_remote")` must reject the name.
- all current execution providers must continue to work unchanged.
- the repository test suite must pass without legacy compatibility tests.

Do not replace the legacy provider with a stub or compatibility alias.
