"""Offline regression tests; no real credentials or provider requests."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/hermes-free-first-setup/scripts/setup_free_first.py'


def model(identifier, pricing=None, tools=True, image=False):
    return {'id': identifier, 'pricing': pricing if pricing is not None else {'prompt': '0', 'completion': '0'},
            'supported_parameters': ['tools'] if tools else [],
            'architecture': {'input_modalities': ['text', 'image'] if image else ['text']}}


class SetupTests(unittest.TestCase):
    def load(self):
        self.assertTrue(SCRIPT.exists(), 'The reusable setup script has not been implemented.')
        spec = importlib.util.spec_from_file_location('free_first_setup', SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_catalog_requires_explicit_zero_prices_and_tool_support(self):
        setup = self.load()
        good = model('vendor/free:free')
        bad = [model('vendor/paid:free', {'prompt': '0.001', 'completion': '0'}),
               model('vendor/missing:free', {}),
               model('vendor/negative:free', {'prompt': '-1', 'completion': '0'}),
               model('vendor/nan:free', {'prompt': 'NaN', 'completion': '0'}),
               model('vendor/fee:free', {'prompt': '0', 'completion': '0', 'request': '1'}),
               model('vendor/no-tools:free', tools=False)]
        self.assertEqual(setup.free_models({'data': [good, *bad]}), {good['id']: good})


    def test_plan_pins_every_discovered_aux_route_and_clears_old_endpoints(self):
        setup = self.load()
        primary = model('vendor/free:free')
        router = model('openrouter/free', image=True)
        snapshot = {'model': {'aliases': {'manualpaid': 'some/paid'}},
                    'auxiliary': {'compression': {'provider': 'custom', 'base_url': 'https://old', 'api_key': 'MASKED'},
                                  'vision': {'provider': 'paid', 'model': 'paid'},
                                  'background_review': {'provider': 'paid', 'model': 'paid', 'enabled': False}}}
        settings = setup.build_settings(snapshot, {primary['id']: primary, router['id']: router}, primary['id'])
        self.assertEqual(settings['model']['provider'], 'openrouter')
        self.assertEqual(settings['model']['aliases']['manualpaid'], 'some/paid')
        self.assertEqual(settings['auxiliary']['vision']['model'], 'openrouter/free')
        for name in ['compression', 'vision', 'background_review']:
            route = settings['auxiliary'][name]
            self.assertEqual(route['provider'], 'openrouter')
            self.assertEqual(route['base_url'], '')
            self.assertEqual(route['api_key'], '')
            self.assertEqual(route['fallback_chain'], [])
        self.assertFalse(settings['auxiliary']['background_review']['enabled'])
        self.assertEqual(settings['delegation']['fallback_providers'], [])
        self.assertEqual(settings['cron.model_provider'], 'openrouter')
        self.assertEqual(settings['cron.model'], primary['id'])
        self.assertEqual(settings['fallback_model'], None)

    def test_plan_rejects_paid_or_unavailable_requested_model(self):
        setup = self.load()
        with self.assertRaises(ValueError):
            setup.build_settings({}, {'openrouter/free': model('openrouter/free', image=True)}, 'vendor/paid')


    def test_transaction_restores_original_config_on_cli_failure(self):
        setup = self.load()
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            config = home / 'config.yaml'
            original = b'model: original\ncustom: keep\n'
            config.write_bytes(original)
            def fail_after_write(_home, args, _exe):
                config.write_text('model: partially-changed\n')
                raise RuntimeError('intentional test CLI failure')
            with patch.object(setup, 'call_cli', fail_after_write):
                with self.assertRaises(RuntimeError):
                    setup.apply_settings(home, {'model': {'provider': 'openrouter'}})
            self.assertEqual(config.read_bytes(), original)
            backups = list((home / 'backups/free-first').glob('*/config.yaml'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), original)
            self.assertFalse((home / '.free-first-setup.lock').exists())
            if os.name != 'nt':
                self.assertEqual(backups[0].stat().st_mode & 0o777, 0o600)

    def test_transaction_removes_new_partial_config_on_failure(self):
        setup = self.load()
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            def fail(_home, _args, _exe):
                (home / 'config.yaml').write_text('partial: true')
                raise RuntimeError('intentional test failure')
            with patch.object(setup, 'call_cli', fail):
                with self.assertRaises(RuntimeError):
                    setup.apply_settings(home, {'model': {}})
            self.assertFalse((home / 'config.yaml').exists())

    def test_refuses_symlink_config_and_existing_setup_lock(self):
        setup = self.load()
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            other = home / 'outside.yaml'
            other.write_text('keep: true')
            (home / 'config.yaml').symlink_to(other)
            with self.assertRaises(ValueError):
                setup.apply_settings(home, {'model': {}})
            (home / 'config.yaml').unlink()
            (home / '.free-first-setup.lock').mkdir()
            with self.assertRaises((ValueError, FileExistsError)):
                setup.apply_settings(home, {'model': {}})
            self.assertEqual(other.read_text(), 'keep: true')

    def test_dry_run_writes_nothing_and_reports_remaining_audit(self):
        setup = self.load()
        primary = model('openrouter/free', image=True)
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / 'uncreated'
            snapshot = {'auxiliary': {'compression': {'provider': 'auto', 'model': ''}}}
            with patch.object(setup, 'fetch_catalog', return_value={'data': [primary]}), \
                 patch.object(setup, 'read_settings', return_value=snapshot), \
                 patch.object(setup, 'check_cli'), \
                 patch.object(setup, 'apply_settings') as write, \
                 patch('sys.stdout'):
                self.assertEqual(setup.main(['--home', str(home)]), 0)
                write.assert_not_called()
            self.assertFalse(home.exists())

    def test_apply_requires_explicit_noninteractive_consent(self):
        setup = self.load()
        with patch('sys.stderr'):
            self.assertNotEqual(setup.main(['--apply']), 0)

    def test_mismatch_after_write_triggers_rollback(self):
        setup = self.load()
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            path = home / 'config.yaml'
            original = b'original: true\n'
            path.write_bytes(original)
            with patch.object(setup, 'call_cli', return_value=''), \
                 patch.object(setup, 'read_settings', return_value={'model': {'provider': 'paid'}}):
                with self.assertRaises(RuntimeError):
                    setup.apply_settings(home, {'model': {'provider': 'openrouter'}})
            self.assertEqual(path.read_bytes(), original)


    def test_read_settings_queries_named_sections(self):
        setup = self.load()
        calls = []
        def cli(_home, args, _exe):
            calls.append(args)
            return json.dumps({'compression': {'provider': 'auto', 'model': ''}} if args[2] == 'auxiliary' else None)
        with patch.object(setup, 'call_cli', cli):
            snapshot = setup.read_settings(Path('/unused'))
        self.assertIn('auxiliary', snapshot)
        self.assertTrue(all(args[:2] == ['config', 'get'] and len(args) == 4 for args in calls))
        self.assertIn(['config', 'get', 'provider_routing', '--json'], calls)


    def test_unset_of_missing_legacy_fallback_is_idempotent(self):
        setup = self.load()
        result = subprocess.CompletedProcess([], 1, '', 'Config key not set: fallback_model\n')
        with patch.object(setup.subprocess, 'run', return_value=result):
            self.assertEqual(setup.call_cli(Path('/unused'), ['config', 'unset', 'fallback_model']), 'null')


    def test_cli_string_values_are_not_json_quoted(self):
        setup = self.load()
        commands = []
        def cli(_home, args, _exe):
            commands.append(args)
            return ''
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(setup, 'call_cli', cli), \
             patch.object(setup, 'read_settings', return_value={'cron': {'model_provider': 'openrouter'}}):
            setup.apply_settings(Path(directory), {'cron.model_provider': 'openrouter'})
        self.assertIn(['config', 'set', 'cron.model_provider', 'openrouter'], commands)


    def test_model_container_uses_documented_deliberate_replace_flag(self):
        setup = self.load()
        commands = []
        route = {'provider': 'openrouter'}
        def cli(_home, args, _exe):
            commands.append(args)
            return ''
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(setup, 'call_cli', cli), \
             patch.object(setup, 'read_settings', return_value={'model': route}):
            setup.apply_settings(Path(directory), {'model': route})
        self.assertIn(['config', 'set', '--force', 'model', json.dumps(route)], commands)


    def test_malformed_optional_catalog_fields_fail_closed(self):
        setup = self.load()
        item = model('vendor/free:free')
        item['supported_parameters'] = None
        self.assertEqual(setup.free_models({'data': [item]}), {})

    def test_empty_expected_override_must_really_be_empty(self):
        setup = self.load()
        self.assertFalse(setup.contains({'models': ['paid']}, {}))

    def test_catalog_failure_never_applies(self):
        setup = self.load()
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(setup, 'check_cli'), \
             patch.object(setup, 'read_settings', return_value={}), \
             patch.object(setup, 'fetch_catalog', side_effect=OSError('test outage')), \
             patch.object(setup, 'apply_settings') as apply, patch('sys.stderr'):
            self.assertEqual(setup.main(['--home', directory, '--apply', '--yes']), 1)
            apply.assert_not_called()

    def test_custom_upstream_routing_is_not_silently_overwritten(self):
        setup = self.load()
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(setup, 'check_cli'), \
             patch.object(setup, 'read_settings', return_value={'providers': {'openrouter': {'base_url': 'https://custom'}}}), \
             patch.object(setup, 'fetch_catalog') as catalog, \
             patch.object(setup, 'apply_settings') as apply, patch('sys.stderr'):
            self.assertEqual(setup.main(['--home', directory, '--apply', '--yes']), 1)
            catalog.assert_not_called()
            apply.assert_not_called()


    def test_complex_alias_credentials_are_not_rewritten_from_masked_reads(self):
        setup = self.load()
        router = model('openrouter/free', image=True)
        with self.assertRaises(ValueError):
            setup.build_settings({'model': {'aliases': {'custom': {'api_key': 'MASKED'}}},
                                  'auxiliary': {'compression': {'provider': 'auto'}}},
                                 {router['id']: router}, router['id'])


    def test_nous_preset_uses_nous_catalog_models_and_endpoint(self):
        setup = self.load()
        primary = model('poolside/laguna-s-2.1:free')
        backup = model('poolside/laguna-xs-2.1:free')
        vision = model('stepfun/step-3.7-flash:free', image=True)
        allowed = {item['id']: item for item in [primary, backup, vision]}
        state = {'auxiliary': {'compression': {'provider': 'auto'}, 'vision': {'provider': 'auto'}}}
        settings = setup.build_settings(state, allowed, primary['id'], provider='nous')
        self.assertEqual(settings['model']['provider'], 'nous')
        self.assertEqual(settings['model']['base_url'], 'https://inference-api.nousresearch.com/v1')
        self.assertEqual(settings['fallback_providers'], [{'provider': 'nous', 'model': backup['id']}])
        self.assertEqual(settings['auxiliary']['vision']['model'], vision['id'])
        self.assertEqual(settings['auxiliary']['vision']['provider'], 'nous')
        self.assertEqual(settings['cron.model_provider'], 'nous')
        self.assertEqual(settings['delegation']['provider'], 'nous')
        self.assertEqual(settings['model']['aliases']['free'], 'nous/' + primary['id'])


if __name__ == '__main__':
    unittest.main()
