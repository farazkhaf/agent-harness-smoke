# Extract the legacy remote execution provider

Batchline still supports the `legacy_remote` execution provider, but its compatibility implementation no longer belongs inline with the current providers.

Move `LegacyRemoteProvider` from `src/batchline/execution/providers.py` into a new module at `src/batchline/execution/legacy_remote.py`.

After the change:

- `LegacyRemoteProvider` and its implementation must live in `legacy_remote.py`, not in `providers.py`.
- `provider_names()` must still include `legacy_remote`.
- `get_provider("legacy_remote")` must continue to return a working legacy provider with the same behavior.
- all current execution providers must continue to work unchanged.
- the repository test suite must pass.

Do not duplicate the implementation in both modules and do not replace it with a stub or compatibility proxy.
