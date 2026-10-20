#!/usr/bin/env python3
"""Package the setup helper and portable skill without caches or credentials."""
from pathlib import Path
import zipfile
import shutil

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/hermes-free-first-setup'
OUT = ROOT / 'downloads'


def main():
    OUT.mkdir(exist_ok=True)
    # Keep the standalone skill's provider reference synchronized with the handbook source.
    shutil.copyfile(ROOT / 'docs/PROVIDER-CHAPTERS.md', SKILL / 'references/PROVIDERS.md')
    sources = sorted(path for path in SKILL.rglob('*')
                     if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc')
    assert sources and (SKILL / 'SKILL.md') in sources
    skill_zip = OUT / 'hermes-free-first-setup-skill.zip'
    with zipfile.ZipFile(skill_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sources:
            archive.write(path, Path(SKILL.name) / path.relative_to(SKILL))
    kit_zip = OUT / 'hermes-free-first-setup-kit.zip'
    with zipfile.ZipFile(kit_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.write(SKILL / 'references/SETUP.md', 'README.md')
        for path in sources:
            archive.write(path, path.relative_to(ROOT))
        for relative in ['scripts/setup_free_first.py', 'docs/SETUP.md', 'docs/PROVIDER-STATUS.md',
                         'downloads/HERMES-FULL-FREE-API-HANDBOOK.pdf',
                         'tests/test_setup_free_first.py', 'tests/test_skill_contract.py',
                         'tests/integration_setup.py']:
            archive.write(ROOT / relative, relative)
    for path in [skill_zip, kit_zip]:
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
            assert not any('__pycache__' in name or name.endswith(('.env', 'auth.json'))
                           for name in archive.namelist())
            print(path.name, 'files:', len(archive.namelist()), 'bytes:', path.stat().st_size)


if __name__ == '__main__':
    main()
