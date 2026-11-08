"""Regression tests exercise disposable repositories, never the user's checkout."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]


def load_module(name, path):
  spec = importlib.util.spec_from_file_location(name, path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


checks = load_module('repo_checks', ROOT / 'scripts/ci/repo_checks.py')


class RepositoryTests(unittest.TestCase):
  def setUp(self):
    self.temporary = tempfile.TemporaryDirectory(prefix='base-tests-')
    self.addCleanup(self.temporary.cleanup)
    self.root = Path(self.temporary.name).resolve()
    self.run_command('git', 'init', '-q', '-b', 'main')
    self.run_command('git', 'config', 'user.name', 'Template Tests')
    self.run_command('git', 'config', 'user.email', 'tests@example.invalid')

  def run_command(self, *args, check=True):
    return subprocess.run(args, cwd=self.root, text=True, capture_output=True, check=check)

  def write(self, name, content):
    path = self.root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path

  def copy(self, name):
    destination = self.root / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / name, destination)
    return destination

  def test_code_labels_and_heading_fragments_are_checked(self):
    self.write('README.md', '# Home\n[`missing`](missing.md)\n[Heading](target.md#absent)\n')
    self.write('target.md', '# Target\n')
    errors = checks.check_links(self.root)
    self.assertEqual(len(errors), 2, errors)

  def test_fences_inline_examples_references_and_encoded_paths(self):
    self.write('README.md', '''# Home
````markdown
```bash
[example](missing.md)
```
````
~~~text
[example](missing.md)
~~~
`[example](missing.md)`
[reference][doc]
[doc]: target.md#target
[space](my%20file.md)
[angle](<my file.md>)
[balanced](thing(one).md)
''')
    self.write('target.md', '# Target\n')
    self.write('my file.md', '# File\n')
    self.write('thing(one).md', '# Thing\n')
    self.assertEqual(checks.check_links(self.root), [])

  def test_undefined_reference_is_rejected(self):
    self.write('README.md', '# Home\n[missing][undefined]\n')
    self.assertTrue(checks.check_links(self.root))

  def test_github_directory_is_checked_but_dependency_trees_are_skipped(self):
    self.write('.github/PULL_REQUEST_TEMPLATE.md', '# PR\n[broken](missing.md)\n')
    self.write('node_modules/package/README.md', '[broken](missing.md)')
    errors = checks.check_links(self.root)
    self.assertEqual(len(errors), 1, errors)
    self.assertIn('.github/', errors[0])

  def test_document_registration_and_hub_reachability(self):
    self.write('docs/README.md', '# Docs\n')
    self.write('docs/guides/README.md', '# Guides\n')
    self.write('docs/guides/task.md', '# Task\n[Docs](../README.md) > [Guides](README.md)\n\n## Related Documents\n[Guide](README.md)\n')
    errors = checks.check_docs(self.root)
    self.assertTrue(any('registration' in e for e in errors), errors)
    self.assertTrue(any('unreachable' in e for e in errors), errors)
    self.write('docs/README.md', '# Docs\n[Guides](guides/README.md)\n')
    self.write('docs/guides/README.md', '# Guides\n[Task](task.md)\n')
    self.assertEqual(checks.check_docs(self.root), [])

  def test_markdown_structure_failures(self):
    self.write('README.md', '# Home\n### Skipped\n# Second\n```\nexample\n```\n')
    errors = checks.check_docs(self.root)
    self.assertEqual(len(errors), 3, errors)

  def test_links_cannot_escape_repository(self):
    self.write('README.md', '# Home\n[Escape](../outside.md)\n')
    self.assertTrue(any('escapes repository' in e for e in checks.check_links(self.root)))

  def test_root_policy_navigation(self):
    self.write('README.md', '# Home\n')
    self.write('SECURITY.md', '# Security\n')
    errors = checks.check_docs(self.root)
    self.assertTrue(any('breadcrumb' in e for e in errors), errors)
    self.assertTrue(any('Related Documents' in e for e in errors), errors)
    self.write('SECURITY.md', '# Security\n[Home](README.md) > Security\n\n## Related Documents\n[Home](README.md)\n')
    self.assertEqual(checks.check_docs(self.root), [])

  def test_unclosed_fence_is_reported(self):
    self.write('README.md', '# Home\n```text\nunfinished\n')
    self.assertTrue(any('unclosed' in e for e in checks.check_docs(self.root)))

  def test_duplicate_heading_anchors_and_comments(self):
    self.write('README.md', '# Home\n[Repeat](target.md#repeat-1)\n<!-- [Ignored](missing.md) -->\n')
    self.write('target.md', '# Target\n## Repeat\n## Repeat\n')
    self.assertEqual(checks.check_links(self.root), [])

  def test_wrappers_run_from_another_directory_without_source_changes(self):
    for name in ['scripts/ci/repo_checks.py', 'scripts/ci/check-docs.sh', 'scripts/ci/check-links.sh']:
      self.copy(name)
    self.write('README.md', '# Home\n')
    before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*')
              if p.is_file() and '.git' not in p.relative_to(self.root).parts}
    for name in ['check-docs.sh', 'check-links.sh']:
      result = subprocess.run(['bash', str(self.root / 'scripts/ci' / name)], cwd=self.root.parent,
                              capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
    after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*')
             if p.is_file() and '.git' not in p.relative_to(self.root).parts}
    self.assertEqual(before, after)
    self.write('README.md', '# Home\n[Broken](absent.md)\n')
    result = self.run_command('bash', 'scripts/ci/check-links.sh', check=False)
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('absent.md', result.stderr)

  def test_secret_filenames_and_examples(self):
    self.copy('.gitignore')
    private = ['.env', '.env.production', 'service/prod.env', 'id_rsa',
               'id_ed25519', 'keys/private.key', 'keys/private.pem', 'keys/private.p12']
    examples = ['.env.example', '.env.production.example', 'service/prod.env.example']
    for name in private:
      with self.subTest(name=name):
        self.assertTrue(checks.secret_path(name))
        self.assertEqual(self.run_command('git', 'check-ignore', name, check=False).returncode, 0)
    for name in examples:
      with self.subTest(name=name):
        self.assertFalse(checks.secret_path(name))
        self.assertEqual(self.run_command('git', 'check-ignore', name, check=False).returncode, 1)

  def test_secret_check_uses_index_and_never_prints_contents(self):
    self.write('service/.env.test', 'fixture value must not appear in output\n')
    self.write('.env.example', 'PUBLIC_SETTING=placeholder\n')
    self.run_command('git', 'add', 'service/.env.test', '.env.example')
    errors = checks.check_secrets(self.root)
    self.assertEqual(len(errors), 1, errors)
    self.assertIn('service/.env.test', errors[0])
    self.assertNotIn('fixture value', errors[0])
    self.run_command('git', 'rm', '--cached', 'service/.env.test')
    self.assertEqual(checks.check_secrets(self.root), [])

  def foundation(self):
    for name in checks.REQUIRED_FILES:
      self.copy(name)
    self.copy('.githooks/commit-msg')
    self.copy('scripts/dev/setup.sh')

  def test_repository_baseline_does_not_require_secret_or_ci_implementation(self):
    self.foundation()
    self.assertFalse((self.root / '.env.example').exists())
    self.assertFalse((self.root / '.github/workflows').exists())
    self.assertEqual(checks.check_repository(self.root), [])
    (self.root / 'LICENSE').unlink()
    self.assertIn('Missing foundation file: LICENSE', checks.check_repository(self.root))

  def test_permissions_are_reported_without_repair(self):
    self.foundation()
    path = self.root / 'scripts/dev/setup.sh'
    path.chmod(0o644)
    errors = checks.check_repository(self.root)
    self.assertTrue(any('must be executable' in error for error in errors), errors)
    self.assertEqual(path.stat().st_mode & 0o111, 0)

  def test_workflow_refs_require_full_sha_in_both_extensions(self):
    self.foundation()
    for extension in ['yml', 'yaml']:
      path = self.write(f'.github/workflows/check.{extension}',
                        "steps:\n  - uses: 'actions/checkout@v4'\n")
      self.assertTrue(any('full commit SHA' in error for error in checks.check_repository(self.root)))
      path.write_text('steps:\n  - uses: actions/checkout@' + 'a' * 40 + '\n  - uses: ./local-action\n')
      self.assertEqual(checks.check_repository(self.root), [])

  def test_reusable_workflow_refs_are_checked(self):
    self.foundation()
    path = self.write('.github/workflows/reuse.yml',
                      'jobs:\n  check:\n    uses: owner/project/.github/workflows/check.yml@main\n')
    self.assertTrue(any('full commit SHA' in error for error in checks.check_repository(self.root)))
    path.write_text('jobs:\n  check:\n    uses: owner/project/.github/workflows/check.yml@' + 'b' * 40 + '\n')
    self.assertEqual(checks.check_repository(self.root), [])

  def test_new_entry_points_report_cli_failures(self):
    for name in ['scripts/ci/repo_checks.py', 'scripts/ci/check-secrets.sh', 'scripts/ci/check-repository.sh']:
      self.copy(name)
    self.foundation()
    for name in ['check-secrets.sh', 'check-repository.sh']:
      result = self.run_command('bash', f'scripts/ci/{name}')
      self.assertEqual(result.returncode, 0, result.stderr)
    self.write('.env', 'fixture only\n')
    self.run_command('git', 'add', '-f', '.env')
    result = self.run_command('bash', 'scripts/ci/check-secrets.sh', check=False)
    self.assertNotEqual(result.returncode, 0)
    self.assertNotIn('fixture only', result.stderr)
    (self.root / 'README.md').unlink()
    result = self.run_command('bash', 'scripts/ci/check-repository.sh', check=False)
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('README.md', result.stderr)


if __name__ == '__main__':
  unittest.main()
