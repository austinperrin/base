"""Exercise the exact metadata-validation code embedded in the title workflow."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / '.github/workflows/pr-title.yml'


class PrTitleTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory(prefix='base-pr-title-')
    self.addCleanup(self.workspace.cleanup)
    self.root = Path(self.workspace.name)
    source = WORKFLOW.read_text()
    match = re.search(r"python3 - <<'PYTHON'\n(.*?)\n          PYTHON", source, re.S)
    self.assertIsNotNone(match, 'Title workflow must expose its tested validation block')
    self.code = textwrap.dedent(match[1])
    self.event = self.root / 'event.json'

  def validate(self, title=None, payload=None):
    self.event.write_text(json.dumps(payload if payload is not None else {'pull_request': {'title': title}}))
    env = dict(os.environ, GITHUB_EVENT_PATH=str(self.event))
    return subprocess.run([sys.executable, '-c', self.code], cwd=self.root, env=env,
                          capture_output=True, text=True)

  def test_all_repository_types_are_accepted(self):
    for kind in 'feat fix docs style refactor perf test build ci chore revert'.split():
      with self.subTest(kind=kind):
        result = self.validate(f'{kind}: describe change')
        self.assertEqual(result.returncode, 0, result.stderr)

  def test_optional_scope_and_breaking_marker(self):
    for title in ['feat(api)!: change contract', 'docs(adr): record decision', 'fix!: correct behavior']:
      with self.subTest(title=title):
        self.assertEqual(self.validate(title).returncode, 0)

  def test_invalid_titles_are_rejected(self):
    for title in ['', 'wip', 'unknown: change', 'docs:', 'docs:   ',
                  'docs(): change', 'docs(bad scope): change', 'docs: first\nsecond',
                  'docs: first\rsecond', None, 42]:
      with self.subTest(title=title):
        result = self.validate(title)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Use a Conventional Commits title', result.stderr)

  def test_shell_syntax_in_title_is_data_and_is_not_echoed(self):
    title = 'fix: $(touch injected) ${{ secrets.EXAMPLE }} "quoted"'
    result = self.validate(title)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertFalse((self.root / 'injected').exists())
    self.assertNotIn(title, result.stdout + result.stderr)

  def test_bad_event_data_fails_with_useful_error(self):
    for payload in [{}, {'pull_request': {}}, {'pull_request': []}]:
      with self.subTest(payload=payload):
        result = self.validate(payload=payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('event metadata', result.stderr)
    self.event.write_text('invalid JSON')
    result = subprocess.run([sys.executable, '-c', self.code], cwd=self.root,
                            env=dict(os.environ, GITHUB_EVENT_PATH=str(self.event)),
                            capture_output=True, text=True)
    self.assertNotEqual(result.returncode, 0)
    self.assertNotIn('Traceback', result.stderr)

  def test_title_and_local_hook_agree_on_representative_subjects(self):
    message = self.root / 'message.txt'
    for title in ['docs: explain change', 'feat(api)!: change contract', 'revert: undo change',
                  'wip', 'docs(): change', 'docs:   ', 'unknown: change']:
      with self.subTest(title=title):
        message.write_text(title + '\n')
        hook = subprocess.run(['bash', str(ROOT / '.githooks/commit-msg'), str(message)],
                              capture_output=True, text=True)
        self.assertEqual(hook.returncode == 0, self.validate(title).returncode == 0)


if __name__ == '__main__':
  unittest.main()
