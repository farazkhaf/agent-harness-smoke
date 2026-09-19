from pathlib import Path
import ast
import os
import subprocess
import sys

APP = Path('/app')
SOURCE = APP / 'src/batchline/execution/providers.py'
CURRENT = {'local', 'thread_pool', 'container', 'sandbox', 'batch_file', 'container_pool'}


def fail(message: str) -> None:
    print(f'FAIL: {message}')
    raise SystemExit(1)


def _class_declares_legacy_provider(node: ast.ClassDef) -> bool:
    """Return true for a class that still declares the retired provider name.

    This is intentionally structural rather than a blanket source-string ban:
    comments, documentation, and negative regression tests may still mention
    ``legacy_remote`` after the implementation is removed.
    """
    for statement in node.body:
        if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
            continue
        targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
        if not any(isinstance(target, ast.Name) and target.id == 'name' for target in targets):
            continue
        value = statement.value
        if isinstance(value, ast.Constant) and value.value == 'legacy_remote':
            return True
    return False


def main() -> None:
    text = SOURCE.read_text(encoding='utf-8')
    tree = ast.parse(text)
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    class_names = {node.name for node in classes}
    if 'LegacyRemoteProvider' in class_names:
        fail('LegacyRemoteProvider class is still defined')
    if any(_class_declares_legacy_provider(node) for node in classes):
        fail('a provider class still declares name = "legacy_remote"')

    sys.path.insert(0, str(APP / 'src'))
    from batchline.execution import ExecutionRequest, get_provider, provider_names

    names = set(provider_names())
    if names != CURRENT:
        fail(f'provider_names changed unexpectedly: {sorted(names)}')
    try:
        get_provider('legacy_remote')
    except KeyError:
        pass
    else:
        fail('get_provider("legacy_remote") still succeeds')

    request = ExecutionRequest(
        job_id='job-verify', kind='thumbnail', queue='media', command=('python', 'worker.py')
    )
    for name in sorted(CURRENT):
        plan = get_provider(name).plan(request)
        if plan.provider != name:
            fail(f'provider {name} returned plan for {plan.provider}')

    result = subprocess.run(
        [sys.executable, '-m', 'pytest', '-q'],
        cwd=APP,
        env={**os.environ, 'PYTHONPATH': '/app/src'},
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        fail(f'repository tests failed: {result.stdout}{result.stderr}')
    print('PASS')


if __name__ == '__main__':
    main()
