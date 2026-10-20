"""Contract checks for the portable skill and its bundled resources."""
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/hermes-free-first-setup'


class SkillContractTests(unittest.TestCase):
    def test_skill_frontmatter_and_resources(self):
        text = (SKILL / 'SKILL.md').read_text()
        self.assertTrue(text.startswith('---\n'))
        self.assertIn('\n---\n', text[4:])
        description = re.search(r'^description: "([^"]+)"$', text, re.M)
        self.assertIsNotNone(description)
        assert description is not None
        self.assertLessEqual(len(description.group(1)), 60)
        for name in ['scripts/setup_free_first.py', 'references/SETUP.md', 'references/POLICY.md']:
            self.assertTrue((SKILL / name).is_file())
        self.assertNotRegex(text, r'/home/[^/]+/')

    def test_skill_scenarios_preserve_permission_and_privacy_requirements(self):
        cases = json.loads((SKILL / 'evals/evals.json').read_text())['evals']
        self.assertEqual(len(cases), 3)
        text = (SKILL / 'SKILL.md').read_text()
        for phrase in ['--apply --yes', 'No paid cron', 'configuration verified; authenticated inference not tested',
                       'merge instead of overwriting', 'existing per-job', 'private-only']:
            self.assertIn(phrase.lower(), text.lower())

    def test_portable_entrypoint_has_no_secret_or_paid_flags(self):
        result = subprocess.run([sys.executable, str(SKILL / 'scripts/setup_free_first.py'), '--help'],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertIn('--home', result.stdout)
        self.assertIn('--apply', result.stdout)
        self.assertNotIn('--api-key', result.stdout)
        self.assertNotIn('--paid', result.stdout)


if __name__ == '__main__':
    unittest.main()
