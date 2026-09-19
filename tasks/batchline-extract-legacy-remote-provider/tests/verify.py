from pathlib import Path
import ast
import inspect
import os
import subprocess
import sys

APP = Path('/app')
PROVIDERS = APP / 'src/batchline/execution/providers.py'
LEGACY = APP / 'src/batchline/execution/legacy_remote.py'
CURRENT = {'local', 'thread_pool', 'container', 'sandbox', 'batch_file', 'container_pool'}
EXPECTED = CURRENT | {'legacy_remote'}


def fail(message: str) -> None:
    print(f'FAIL: {message}')
    raise SystemExit(1)


def defined_class_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8'))
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}


def main() -> None:
    if not LEGACY.exists():
        fail('src/batchline/execution/legacy_remote.py was not created')

    # The old module may import LegacyRemoteProvider for registry wiring, but it
    # must no longer *define* the implementation there.
    if 'LegacyRemoteProvider' in defined_class_names(PROVIDERS):
        fail('LegacyRemoteProvider is still defined in providers.py')

    # Distinctive legacy-only implementation details should leave providers.py.
    # These checks prevent a nominal wrapper in the new module from leaving the
    # substantial compatibility implementation behind in the old module.
    providers_text = PROVIDERS.read_text(encoding='utf-8')
    legacy_residue = (
        'batchline-remote-runner',
        'BATCHLINE_REMOTE_TOKEN',
        'BATCHLINE_LEGACY_REMOTE',
        'upload_chunk_kb',
        'download_chunk_kb',
        'def migration_hint(',
        'def compatibility_flags(',
    )
    for marker in legacy_residue:
        if marker in providers_text:
            fail(f'legacy implementation residue remains in providers.py: {marker}')

    sys.path.insert(0, str(APP / 'src'))
    from batchline.execution import ExecutionRequest, get_provider, provider_names

    names = set(provider_names())
    if names != EXPECTED:
        fail(f'provider_names changed unexpectedly: {sorted(names)}')

    provider = get_provider('legacy_remote')
    if type(provider).__name__ != 'LegacyRemoteProvider':
        fail(f'legacy provider class was renamed unexpectedly: {type(provider).__name__}')
    provider_source = inspect.getsourcefile(type(provider))
    if provider_source is None or Path(provider_source).resolve() != LEGACY.resolve():
        fail(f'legacy provider implementation is not loaded from legacy_remote.py: {provider_source}')

    # Verify the supported public behavior, not how methods are arranged in the
    # class body. Inherited methods and locally factored helpers are acceptable.
    for member in ('plan', 'migration_hint', 'compatibility_flags', 'with_region', 'with_project', 'with_endpoint'):
        if not callable(getattr(provider, member, None)):
            fail(f'legacy provider public behavior is incomplete: {member} is not callable')

    request = ExecutionRequest(
        job_id='job-verify',
        kind='thumbnail',
        queue='media',
        command=('python', 'worker.py'),
        environment={'MODE': 'verify'},
        trace_id='trace-verify',
    )
    plan = provider.plan(request)
    if plan.provider != 'legacy_remote':
        fail(f'legacy provider returned plan for {plan.provider}')
    if plan.cwd != '/app':
        fail(f'legacy provider cwd changed unexpectedly: {plan.cwd}')
    if '--project' not in plan.argv or 'default' not in plan.argv:
        fail('legacy provider default project behavior changed')
    if '--region' not in plan.argv or 'local' not in plan.argv:
        fail('legacy provider default region behavior changed')
    if plan.argv[-2:] != ('python', 'worker.py'):
        fail('legacy provider command forwarding changed')
    if plan.labels.get('batchline.execution_mode') != 'legacy-remote':
        fail('legacy provider execution label changed')
    if not provider.migration_hint().startswith('legacy_remote is deprecated'):
        fail('legacy provider migration hint changed')

    flags = provider.compatibility_flags(request)
    if '--project' not in flags or 'default' not in flags or '--region' not in flags or 'local' not in flags:
        fail('legacy provider compatibility flags changed')
    if tuple(request.command) == tuple(flags[-len(request.command):]):
        fail('compatibility_flags unexpectedly includes the final user command')

    moved_region = provider.with_region('eu-test')
    if moved_region.region != 'eu-test' or moved_region.project != provider.project:
        fail('legacy provider region cloning behavior changed')

    moved_project = provider.with_project('project-test')
    if moved_project.project != 'project-test' or moved_project.region != provider.region:
        fail('legacy provider project cloning behavior changed')

    moved_endpoint = provider.with_endpoint('https://example.invalid/v1')
    if moved_endpoint.endpoint != 'https://example.invalid/v1' or moved_endpoint.project != provider.project:
        fail('legacy provider endpoint cloning behavior changed')

    for name in sorted(CURRENT):
        current_plan = get_provider(name).plan(request)
        if current_plan.provider != name:
            fail(f'current provider {name} returned plan for {current_plan.provider}')

    result = subprocess.run(
        [sys.executable, '-m', 'pytest', '-q'],
        cwd=APP,
        env={**os.environ, 'PYTHONPATH': str(APP / 'src')},
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        fail(f'repository tests failed: {result.stdout}{result.stderr}')
    print('PASS')


if __name__ == '__main__':
    main()
