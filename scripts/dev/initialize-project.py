"""Preview or apply the one-time GitHub project initialization changes."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
SOURCE_REPOSITORY = 'austinperrin/base'
SOURCE_URL = f'https://github.com/{SOURCE_REPOSITORY}'
SOURCE_EMAIL = 'perrinaustin@gmail.com'
VERIFICATION_URL = f'{SOURCE_URL}/blob/main/docs/architecture/phase-6-verification.md'

URL_FILES = {
  '.github/ISSUE_TEMPLATE/config.yml': 1,
  '.github/ISSUE_TEMPLATE/bug_report.yml': 1,
  '.github/ISSUE_TEMPLATE/feature_request.yml': 1,
  '.github/PULL_REQUEST_TEMPLATE.md': 2,
}
EMAIL_FILES = ('SECURITY.md', 'CODE_OF_CONDUCT.md')
REMOVALS = (
  'docs/architecture/phase-6-verification.md',
  'docs/runbooks/initialize-repository.md',
  'scripts/dev/initialize-project.py',
  'scripts/dev/tests/test_initialize_project.py',
)


def run_git(*arguments):
  return subprocess.run(
    ['git', *arguments], cwd=ROOT, capture_output=True, text=True, check=False)


def repository_root():
  result = run_git('rev-parse', '--show-toplevel')
  if result.returncode or Path(result.stdout.strip()).resolve() != ROOT:
    raise ValueError('Run this helper from a copy rooted at its Git repository.')
  remote = run_git('remote', 'get-url', 'origin')
  if remote.returncode:
    raise ValueError('Configure the destination as the origin remote first.')
  url = remote.stdout.strip().removesuffix('.git')
  for prefix in ('https://github.com/', 'git@github.com:', 'ssh://git@github.com/'):
    if url.startswith(prefix):
      name = url[len(prefix):]
      if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', name):
        break
      if name.lower() == SOURCE_REPOSITORY:
        raise ValueError('The origin remote still points to the foundation repository.')
      return name
  raise ValueError('The origin remote must identify the new GitHub repository.')


def read_file(name):
  path = ROOT / name
  if path.is_symlink() or not path.is_file():
    raise ValueError(f'Required regular file is missing: {name}')
  return path.read_text(encoding='utf-8')


def replace_count(name, old, new, count):
  content = read_file(name)
  if content.count(old) != count:
    raise ValueError(f'Expected {count} source value(s) in {name}; review edits manually.')
  return content.replace(old, new)


def validate_email(value):
  if not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+', value):
    raise ValueError('Enter a single email address without spaces or markup.')


def configure_plan(repository, security_email, conduct_email):
  if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
    raise ValueError('Use OWNER/REPOSITORY for --repository.')
  if repository.lower() != repository_root().lower():
    raise ValueError('--repository must match the origin remote.')
  validate_email(security_email)
  validate_email(conduct_email)
  if SOURCE_EMAIL in (security_email, conduct_email):
    raise ValueError('Replace the foundation reporting address with a project contact.')
  destination = f'https://github.com/{repository}'
  plan = {
    name: replace_count(name, SOURCE_URL, destination, count)
    for name, count in URL_FILES.items()
  }
  for name, address in (('SECURITY.md', security_email),
                        ('CODE_OF_CONDUCT.md', conduct_email)):
    plan[name] = replace_count(name, SOURCE_EMAIL, address, 2)
  return plan


def tracked_and_unchanged(name):
  tracked = run_git('ls-files', '--error-unmatch', '--', name)
  changed = run_git('diff', '--quiet', 'HEAD', '--', name)
  if tracked.returncode or changed.returncode or (ROOT / name).is_symlink():
    raise ValueError(f'Removal candidate is missing or modified: {name}')
  read_file(name)


def finish_plan():
  repository = repository_root()
  for name in REMOVALS:
    tracked_and_unchanged(name)
  destination = f'https://github.com/{repository}'
  for name, count in URL_FILES.items():
    content = read_file(name)
    if SOURCE_URL in content or content.count(destination) != count:
      raise ValueError(f'Confirm the new repository links in {name} before finishing.')
  for name in EMAIL_FILES:
    if SOURCE_EMAIL in read_file(name):
      raise ValueError('Replace source reporting contacts before finishing setup.')
  readme = read_file('README.md')
  if '# Base Repository Template' in readme or 'initialize-repository.md' in readme:
    raise ValueError('Replace the root README and its setup link before finishing.')
  owners = read_file('.github/CODEOWNERS')
  if '@your-maintainer' in owners or '@your-org' in owners:
    raise ValueError('Assign or remove the example CODEOWNERS accounts before finishing.')

  plan = {}
  name = 'docs/architecture/README.md'
  row = '| [Phase 6 verification record](phase-6-verification.md) | Historical foundation results and remaining verification cases |\n'
  plan[name] = replace_count(name, row, '', 1)

  name = 'docs/roadmap/milestone-0-repository-scaffolding.md'
  plan[name] = replace_count(name, '../architecture/phase-6-verification.md', VERIFICATION_URL, 2)

  name = 'docs/runbooks/README.md'
  row = '| [Initialize a project repository](initialize-repository.md) | Turn the foundation into a new project repository |\n'
  plan[name] = replace_count(name, row, '', 1)

  name = 'scripts/README.md'
  row = '| [initialize-project.py](dev/initialize-project.py) | Previews or applies one-time project setup and cleanup | `python3 scripts/dev/initialize-project.py --help` |\n'
  content = replace_count(name, row, '', 1)
  section = (
    '## One-Time Project Initialization\n\n'
    'The [initialization runbook](../docs/runbooks/initialize-repository.md) owns the\n'
    'setup order. `initialize-project.py configure` previews fixed source URL and\n'
    'reporting-contact replacements; `finish` previews removal of source-only records\n'
    'and the helper itself. Each stage requires `--apply` to write changes. The helper\n'
    'checks the destination GitHub remote, refuses modified removal candidates, and\n'
    'checks documentation after applying changes. It leaves the root README, review\n'
    'owners, ADR outcomes, and live repository settings for the maintainer to resolve.\n\n'
  )
  if content.count(section) != 1:
    raise ValueError('The script-reference setup section changed; review it manually.')
  plan[name] = content.replace(section, '')

  name = 'docs/runbooks/configure-github.md'
  content = read_file(name)
  old = ('- Complete the [identity and contact setup](initialize-repository.md#set-identity-and-reporting-contacts)\n'
         '  for identity and reporting contacts before inviting reports or relying on\n'
         '  the issue forms.\n')
  if old in content:
    content = content.replace(old,
      '- Confirm the project identity and reporting contacts before inviting\n'
      '  reports or relying on the issue forms.\n')
    related = '- [Initialize a project repository](initialize-repository.md) - Identity and reporting-contact setup.\n'
    if content.count(related) != 1:
      raise ValueError('The GitHub runbook setup link changed; review it manually.')
    content = content.replace(related,
      '- [Security policy](../../SECURITY.md) - Private reporting channels.\n')
    plan[name] = content

  for name in REMOVALS:
    plan[name] = None

  for current, directories, files in os.walk(ROOT, followlinks=False):
    directories[:] = [directory for directory in directories
                      if directory != '.git' and not (Path(current) / directory).is_symlink()]
    for filename in files:
      path = Path(current) / filename
      if path.suffix != '.md' or path.is_symlink():
        continue
      name = path.relative_to(ROOT).as_posix()
      content = plan.get(name)
      if content is None and name in plan:
        continue
      content = content if content is not None else path.read_text(encoding='utf-8')
      if 'phase-6-verification.md' in content and name != 'docs/roadmap/milestone-0-repository-scaffolding.md':
        raise ValueError(f'An incoming verification-record link remains in {name}.')
      if 'initialize-repository.md' in content:
        raise ValueError(f'An incoming initialization-runbook link remains in {name}.')
  return plan


def apply_plan(plan):
  originals = {name: (ROOT / name).read_bytes() for name in plan}
  try:
    for name, content in plan.items():
      path = ROOT / name
      if path.read_bytes() != originals[name]:
        raise ValueError(f'{name} changed during setup; no further files were updated.')
      if content is None:
        path.unlink()
      else:
        path.write_text(content, encoding='utf-8')
    for check in ('check-links.sh', 'check-docs.sh'):
      result = subprocess.run(
        [str(ROOT / 'scripts/ci' / check)], cwd=ROOT,
        capture_output=True, text=True, check=False)
      if result.returncode:
        raise ValueError(f'{check} failed after setup:\n{result.stdout}{result.stderr}')
  except (OSError, ValueError):
    for name, content in originals.items():
      (ROOT / name).write_bytes(content)
    raise


def main():
  if sys.version_info < (3, 9):
    raise ValueError('Python 3.9 or newer is required.')
  parser = argparse.ArgumentParser(description=__doc__)
  commands = parser.add_subparsers(dest='command', required=True)
  configure = commands.add_parser('configure', help='Replace source URLs and reporting contacts')
  configure.add_argument('--repository', required=True, help='New GitHub OWNER/REPOSITORY')
  configure.add_argument('--security-email', required=True)
  configure.add_argument('--conduct-email', required=True)
  configure.add_argument('--apply', action='store_true', help='Apply the previewed changes')
  finish = commands.add_parser('finish', help='Remove one-time source records and setup files')
  finish.add_argument('--apply', action='store_true', help='Apply the previewed changes')
  args = parser.parse_args()
  if args.command == 'configure':
    plan = configure_plan(args.repository, args.security_email, args.conduct_email)
  else:
    plan = finish_plan()
  for name, content in plan.items():
    action = 'remove' if content is None else 'update'
    print(f'{"Will" if args.apply else "Would"} {action}: {name}')
  if args.apply:
    apply_plan(plan)
    print('Setup changes applied; review and commit the resulting diff.')
  else:
    print('Preview only. Re-run with --apply after reviewing every path.')


if __name__ == '__main__':
  try:
    main()
  except (OSError, ValueError) as error:
    sys.exit(f'Error: {error}')
