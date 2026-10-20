#!/usr/bin/env python3
"""Opt-in real Hermes CLI test; disposable homes, public catalog, no inference."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/hermes-free-first-setup/scripts/setup_free_first.py'
spec = importlib.util.spec_from_file_location('free_first_setup', SCRIPT)
assert spec is not None and spec.loader is not None
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


def main():
    checks = []
    with tempfile.TemporaryDirectory(prefix='hermes-free-first-integration-') as directory:
        home = Path(directory) / 'profile'
        command = [sys.executable, str(ROOT / 'scripts/setup_free_first.py'), '--home', str(home)]
        def run(flags):
            result = subprocess.run(command + flags, text=True, capture_output=True, timeout=180)
            assert result.returncode == 0, result.stderr
            return json.loads(result.stdout)
        run([])
        assert not home.exists()
        checks.append('dry-run target remains absent')
        first = run(['--apply', '--yes'])
        assert first['configuration_readback'] == 'passed'
        checks.append('fresh real-CLI apply and read-back')
        setup.call_cli(home, ['config', 'set', 'terminal.timeout', '321'])
        original = (home / 'config.yaml').read_bytes()
        sentinels = {'.env': b'DO_NOT_CHANGE=fixture\n', 'auth.json': b'{}\n'}
        for name, value in sentinels.items():
            (home / name).write_bytes(value)
        second = run(['--apply', '--yes'])
        assert (home / 'config.yaml').read_bytes() == original
        assert Path(second['backup']).read_bytes() == original
        for name, value in sentinels.items():
            assert (home / name).read_bytes() == value
        assert json.loads(setup.call_cli(home, ['config', 'get', 'terminal.timeout', '--json'])) == 321
        checks.extend(['byte-idempotent reapply', 'private backup matches original',
                       'unrelated configuration preserved', '.env/auth.json fixture files unchanged'])
        state = setup.read_settings(home)
        settings = setup.build_settings(state, setup.free_models(setup.fetch_catalog()), state['model']['default'])
        actual_call = setup.call_cli
        def fail_midway(target, args, executable='hermes'):
            if args[:3] == ['config', 'set', 'cron.model']:
                raise RuntimeError('Intentional integration-test failure')
            return actual_call(target, args, executable)
        with patch.object(setup, 'call_cli', fail_midway):
            try:
                setup.apply_settings(home, settings)
            except RuntimeError as error:
                assert 'Intentional' in str(error)
            else:
                raise AssertionError('Failure injection did not fire')
        assert (home / 'config.yaml').read_bytes() == original
        assert not (home / '.free-first-setup.lock').exists()
        checks.append('real-CLI partial-write failure restores original config and releases lock')
    print(json.dumps({'checks_passed': len(checks), 'checks': checks,
                      'auxiliary_slots_configured': len(first['auxiliary_slots']),
                      'authenticated_inference': 'not run', 'real_credentials': 'not used'}, indent=2))


if __name__ == '__main__':
    main()
