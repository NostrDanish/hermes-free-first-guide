#!/usr/bin/env python3
"""Configure Hermes for free-first use; stdlib only, no credential handling."""
from decimal import Decimal, InvalidOperation
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen
import uuid


PROVIDERS = {
    'openrouter': {'base_url': 'https://openrouter.ai/api/v1',
                   'preferred': 'nvidia/nemotron-3-ultra-550b-a55b:free',
                   'backup': 'openrouter/free', 'vision': 'openrouter/free'},
    'nous': {'base_url': 'https://inference-api.nousresearch.com/v1',
             'preferred': 'poolside/laguna-s-2.1:free',
             'backup': 'poolside/laguna-xs-2.1:free', 'vision': 'stepfun/step-3.7-flash:free'},
}


def free_models(catalog):
    """Accept only explicit finite zero pricing plus advertised tool support."""
    if not isinstance(catalog, dict) or not isinstance(catalog.get('data'), list):
        raise ValueError('The provider returned an invalid model catalog.')
    result = {}
    for item in catalog['data']:
        if not isinstance(item, dict):
            continue
        prices = item.get('pricing')
        if not isinstance(prices, dict) or not {'prompt', 'completion'} <= prices.keys():
            continue
        try:
            values = [Decimal(str(value)) for value in prices.values()]
            zero = all(value.is_finite() and value == 0 for value in values)
        except (InvalidOperation, ValueError, TypeError):
            continue
        identifier = item.get('id')
        parameters = item.get('supported_parameters')
        if (zero and isinstance(parameters, list) and isinstance(identifier, str) and identifier
                and 'tools' in parameters):
            result[identifier] = item
    return result


def build_settings(snapshot, allowed, primary, provider='openrouter'):
    """Reset automatic routing while preserving unrelated top-level settings."""
    if primary not in allowed:
        raise ValueError('Requested model is absent, priced, or lacks tool support.')
    preset = PROVIDERS[provider]
    if provider == 'openrouter' and 'openrouter/free' not in allowed:
        raise ValueError('The free router is unavailable; refusing an unverified fallback.')
    vision_candidates = [primary, preset['vision'], *sorted(allowed)]
    vision = next((identifier for identifier in vision_candidates if identifier in allowed
                   and 'image' in (allowed[identifier].get('architecture') or {}).get('input_modalities', [])), None)
    if vision is None:
        raise ValueError('No verified free image route is available.')
    backup = preset['backup'] if preset['backup'] in allowed else next(iter(sorted(allowed)), primary)
    fallbacks = [] if primary == backup else [{'provider': provider, 'model': backup}]
    old_model = snapshot.get('model') or {}
    aliases = (old_model.get('aliases') or {}) if isinstance(old_model, dict) else {}
    if not isinstance(aliases, dict) or any(not isinstance(value, str) for value in aliases.values()):
        raise ValueError('Complex model aliases need manual review; refusing to rewrite masked credentials.')
    aliases = dict(aliases)
    aliases['free'] = provider + '/' + primary
    if provider == 'openrouter':
        aliases['freerouter'] = 'openrouter/openrouter/free'
    aux = {'free_only': True, 'openrouter_model': primary}
    slots = snapshot.get('auxiliary') or {}
    if not isinstance(slots, dict):
        raise ValueError('Unrecognized auxiliary configuration.')
    for name, slot in slots.items():
        if isinstance(slot, dict) and ('provider' in slot or 'model' in slot):
            route = {'provider': provider, 'model': vision if name == 'vision' else primary,
                     'base_url': '', 'api_key': '', 'extra_body': {}, 'fallback_chain': []}
            if isinstance(slot.get('enabled'), bool):
                route['enabled'] = slot['enabled']
            aux[name] = route
    if not any(isinstance(value, dict) for value in aux.values()):
        raise ValueError('No auxiliary slots discovered; update Hermes before applying.')
    return {
        'model': {'provider': provider, 'default': primary,
                  'base_url': preset['base_url'], 'api_key': '',
                  'api_mode': 'chat_completions', 'aliases': aliases},
        'fallback_providers': fallbacks,
        'fallback_model': None,
        'delegation': {'provider': provider, 'model': primary, 'base_url': '', 'api_key': '',
                       'fallback_providers': [], 'max_concurrent_children': 2,
                       'subagent_auto_approve': False},
        'cron.model_provider': provider, 'cron.model': primary, 'cron.provider': '',
        'auxiliary': aux,
    }


def call_cli(home, args, executable='hermes'):
    env = os.environ.copy()
    env['HERMES_HOME'] = str(home)
    try:
        result = subprocess.run([executable, *args], env=env, capture_output=True,
                                text=True, timeout=45, check=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError('Hermes CLI failed or timed out; no credential output was captured in the report.') from error
    if (result.returncode and len(args) >= 2 and args[0] == 'config'
            and args[1] in ['get', 'unset'] and result.stderr.startswith('Config key not set:')):
        return 'null'
    if result.returncode:
        # CLI errors can contain configuration values: do not echo stdout/stderr.
        raise RuntimeError('Hermes rejected a configuration operation; inspect its version/help locally.')
    return result.stdout


def check_cli(home, executable='hermes'):
    actual = Path(call_cli(home, ['config', 'path'], executable).strip()).resolve()
    if actual != home / 'config.yaml':
        raise ValueError('Hermes resolved a different profile; refusing to write.')


def read_settings(home, executable='hermes'):
    sections = ['model', 'auxiliary', 'delegation', 'cron', 'fallback_providers',
                'fallback_model', 'providers', 'provider_routing', 'request_overrides']
    return {key: json.loads(call_cli(home, ['config', 'get', key, '--json'], executable))
            for key in sections}


def fetch_catalog(provider='openrouter'):
    request = Request(PROVIDERS[provider]['base_url'] + '/models',
                      headers={'User-Agent': 'hermes-free-first-setup/0.1'})
    with urlopen(request, timeout=30) as response:
        # shortcut: public catalogs over 16 MiB are rejected; raise only after review.
        payload = response.read(16 * 1024 * 1024 + 1)
    if len(payload) > 16 * 1024 * 1024:
        raise ValueError('Model catalog exceeded the safe size limit.')
    return json.loads(payload)


def contains(actual, expected):
    if isinstance(expected, dict):
        if not expected:
            return actual == {}
        return (isinstance(actual, dict)
                and all(key in actual and contains(actual[key], value) for key, value in expected.items()))
    return actual == expected


def apply_settings(home, settings, executable='hermes'):
    """Back up config, use supported CLI writes, verify, roll back on failure."""
    config = home / 'config.yaml'
    if config.is_symlink():
        raise ValueError('Symlinked config is not supported by this installer.')
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = home / '.free-first-setup.lock'
    lock.mkdir(mode=0o700)
    original = None
    backup = None
    started = False
    try:
        if config.exists():
            original = config.read_bytes()
            base = home / 'backups' / 'free-first'
            if any(part.is_symlink() for part in [home / 'backups', base]):
                raise ValueError('Symlinked backup directories are not supported.')
            backup = base / uuid.uuid4().hex
            backup.mkdir(parents=True, mode=0o700)
            os.chmod(backup, 0o700)
            with (backup / 'config.yaml').open('xb') as stream:
                os.chmod(backup / 'config.yaml', 0o600)
                stream.write(original)
        for key, value in settings.items():
            started = True
            if value is None:
                call_cli(home, ['config', 'unset', key], executable)
            else:
                encoded = value if isinstance(value, str) else json.dumps(value)
                # --force is documented for deliberate replacement of an existing section.
                flags = ['--force'] if isinstance(value, dict) else []
                call_cli(home, ['config', 'set', *flags, key, encoded], executable)
        actual = read_settings(home, executable)
        for key, expected in settings.items():
            value = actual
            for part in key.split('.'):
                value = value.get(part) if isinstance(value, dict) else None
            if not contains(value, expected):
                raise RuntimeError('Read-back did not match the requested free-first routes.')
        return str(backup / 'config.yaml') if backup else None
    except BaseException:
        if started:
            if original is None:
                config.unlink(missing_ok=True)
            else:
                fd, name = tempfile.mkstemp(prefix='.free-first-restore-', dir=home)
                try:
                    with os.fdopen(fd, 'wb') as stream:
                        stream.write(original)
                    os.replace(name, config)
                finally:
                    Path(name).unlink(missing_ok=True)
        raise
    finally:
        lock.rmdir()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', required=False,
                        default=os.environ.get('HERMES_HOME', str(Path.home() / '.hermes')),
                        help='Explicit target Hermes data/profile directory; review this before applying.')
    parser.add_argument('--provider', choices=sorted(PROVIDERS), default='openrouter',
                        help='Verified public-catalog preset; does not authenticate the account.')
    parser.add_argument('--model', help='Exact catalog model ID; must pass the live free/tool checks.')
    parser.add_argument('--apply', action='store_true', help='Apply the plan; without this flag nothing is written.')
    parser.add_argument('--yes', action='store_true', help='Confirm replacement of the listed routing settings.')
    args = parser.parse_args(argv)
    if args.apply and not args.yes:
        print('Refusing apply without --yes; first run without --apply to inspect the plan.', file=sys.stderr)
        return 2
    home = Path(args.home).expanduser().resolve()
    if home in [Path(home.anchor), Path.home().resolve()]:
        print('Choose a Hermes data directory, not the filesystem or user-home root.', file=sys.stderr)
        return 2
    try:
        config = home / 'config.yaml'
        if config.is_symlink():
            raise ValueError('Symlinked config is not supported by this installer.')
        original = config.read_bytes() if config.exists() else None
        # Hermes config reads bootstrap files; isolate those side effects from the target.
        with tempfile.TemporaryDirectory(prefix='hermes-free-first-inspect-') as directory:
            probe = Path(directory)
            if original is not None:
                target = probe / 'config.yaml'
                target.touch(mode=0o600)
                target.write_bytes(original)
            check_cli(probe)
            snapshot = read_settings(probe)
        if (snapshot.get('provider_routing') or snapshot.get('request_overrides')
                or (snapshot.get('providers') or {}).get(args.provider)):
            raise ValueError('Custom provider/request routing exists. Review it manually before using this preset.')
        allowed = free_models(fetch_catalog(args.provider))
        preset = PROVIDERS[args.provider]
        preferred = preset['preferred']
        primary = args.model or (preferred if preferred in allowed else preset['backup'])
        settings = build_settings(snapshot, allowed, primary, provider=args.provider)
        report = {
            'mode': 'apply' if args.apply else 'dry-run', 'home': str(home),
            'main': {'provider': args.provider, 'model': primary},
            'vision_model': settings['auxiliary']['vision']['model'] if 'vision' in settings['auxiliary'] else None,
            'managed_sections': list(settings),
            'auxiliary_slots': sorted(key for key, value in settings['auxiliary'].items() if isinstance(value, dict)),
            'changes': [
                'Replace main routing and automatic fallback chains with verified free routes.',
                'Reset delegation routing and cap concurrent children at two.',
                'Set cron fleet defaults; existing per-job pins remain untouched.',
                'Reset discovered auxiliary routing/endpoints; preserve explicit enabled flags.',
                'Keep unrelated top-level settings and existing alias names; update free and the preset-specific shortcut.',
            ],
            'remaining_manual_checks': [
                'Authenticate the selected provider only through its trusted local login/key UI or supported secret source.',
                'Audit pinned cron jobs, worker overrides, other profiles, MCP sampling, plugins and external tool charges.',
                'Select/install local models through Hermes Local Models if desired; none are downloaded here.',
                'No paid auto-escalation is installed. Jev is optional and its hosted API may cost money.',
                'A free route is not a billing firewall. Keep paid credentials isolated and use provider budgets.',
                'Restart/reopen appropriate sessions and test a real completion and tool call; neither is run here.',
            ],
        }
        if args.apply:
            if (config.read_bytes() if config.exists() else None) != original:
                raise ValueError('Configuration changed while planning; rerun before applying.')
            report['backup'] = apply_settings(home, settings)
            report['configuration_readback'] = 'passed'
        print(json.dumps(report, indent=2))
        return 0
    except (ValueError, RuntimeError, OSError) as error:
        # Never print subprocess output, catalog bodies, or loaded configuration.
        detail = str(error) if isinstance(error, (ValueError, RuntimeError)) else type(error).__name__
        print('Setup stopped: ' + detail, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
