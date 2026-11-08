"""Repository checks shared by the shell entry points; Python standard library only."""

import argparse
import fnmatch
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


EXCLUDED = {'.git', 'node_modules', 'vendor', '.cache', '.venv', 'venv',
            'build', 'dist', 'coverage', '__pycache__', 'tmp', '.tmp', 'temp', 'scratch'}


def markdown_files(root):
  for directory, dirs, files in os.walk(root):
    dirs[:] = sorted(d for d in dirs if d not in EXCLUDED and not (Path(directory) / d).is_symlink())
    if Path(directory) == root / '.github' and 'styles' in dirs:
      dirs.remove('styles')
    for name in sorted(files):
      path = Path(directory) / name
      if path.suffix == '.md' and not path.is_symlink():
        yield path


def prose(text):
  """Mask fenced examples and HTML comments while preserving line numbers."""
  result = []
  fence = None
  text = re.sub(r'<!--[\s\S]*?-->', lambda m: '\n' * m[0].count('\n'), text)
  for line in text.splitlines(keepends=True):
    match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
    if fence:
      if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
        fence = None
      result.append('\n')
    elif match:
      fence = match[1]
      result.append('\n')
    else:
      result.append(line)
  return ''.join(result)


def links(text):
  """Read inline and reference links, retaining code-formatted link labels."""
  text = prose(text)
  definitions = {}
  definition = re.compile(r'^ {0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+).*$', re.M)
  for match in definition.finditer(text):
    definitions[' '.join(match[1].lower().split())] = match[2].strip('<>')
  text = definition.sub('', text)
  # Consume a whole link before consuming a code span, so [`file`](file) survives.
  token = re.compile(
    r'`+|!?\[([^\]\n]+)\](?:\((<[^>\n]+>|(?:\\.|[^()\s]|\([^()]*\))+)'
    r'(?:\s+"[^"\n]*")?\)|\[([^\]\n]*)\])?')
  position = 0
  while match := token.search(text, position):
    position = match.end()
    if match[0].startswith('`'):
      close = re.search(r'(?<!`)`{' + str(len(match[0])) + r'}(?!`)', text[position:])
      if close:
        position += close.end()
      continue
    if match[2]:
      yield re.sub(r'\\([\\()])', r'\1', match[2].strip('<>'))
    else:
      key = match[3] or match[1]
      key = ' '.join(key.lower().split())
      if key in definitions:
        yield definitions[key]
      elif match[3] is not None:
        yield 'missing-reference:' + key


def local_target(root, source, url):
  parts = urlsplit(url)
  if parts.scheme or parts.netloc:
    return None
  target = unquote(parts.path)
  return (root / target.lstrip('/') if target.startswith('/') else source.parent / target).resolve() if target else source.resolve()


def headings(text):
  return re.findall(r'^ {0,3}(#{1,6})\s+(.+?)\s*#*$', prose(text), re.M)


def anchors(text):
  used = set()
  for _, title in headings(text):
    title = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', title)
    slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
    candidate, count = slug, 0
    while candidate in used:
      count += 1
      candidate = f'{slug}-{count}'
    used.add(candidate)
  return used


def check_links(root):
  errors = []
  for source in markdown_files(root):
    for url in links(source.read_text(encoding='utf-8')):
      if url.startswith('missing-reference:'):
        errors.append(f'{source.relative_to(root)}: undefined reference {url.split(":", 1)[1]}')
        continue
      target = local_target(root, source, url)
      if target is None:
        continue
      if not target.is_relative_to(root):
        errors.append(f'{source.relative_to(root)}: link escapes repository: {url}')
      elif not target.exists():
        errors.append(f'{source.relative_to(root)}: missing link target: {url}')
      elif urlsplit(url).fragment and target.suffix == '.md':
        fragment = unquote(urlsplit(url).fragment)
        if fragment not in anchors(target.read_text(encoding='utf-8')):
          errors.append(f'{source.relative_to(root)}: missing heading: {url}')
  return errors


def check_docs(root):
  errors = []
  files = list(markdown_files(root))
  graph = {}
  for source in files:
    text = source.read_text(encoding='utf-8')
    outgoing = {local_target(root, source, url) for url in links(text)}
    graph[source.resolve()] = outgoing - {None}
    relative = source.relative_to(root)
    titles = headings(text)
    if sum(len(level) == 1 for level, _ in titles) != 1:
      errors.append(f'{relative}: require exactly one top-level heading')
    if re.search(r'^.+\n {0,3}(?:={3,}|-{3,})\s*$', prose(text), re.M):
      errors.append(f'{relative}: use ATX headings instead of underline headings')
    previous = 0
    for level, _ in titles:
      if len(level) > previous + 1:
        errors.append(f'{relative}: heading skips a level')
      previous = len(level)
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
      match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
      if match:
        if fence and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
          fence = None
        elif not fence:
          fence = match[1]
          if not match[2].strip():
            errors.append(f'{relative}:{number}: fenced block needs a language')
    if fence:
      errors.append(f'{relative}: unclosed fenced block')
    if relative.parts[0] != 'docs':
      if len(relative.parts) == 1 and source.name in {'CONTRIBUTING.md', 'SECURITY.md', 'CODE_OF_CONDUCT.md'}:
        top_links = {local_target(root, source, url) for url in links('\n'.join(text.splitlines()[:5]))}
        if (root / 'README.md').resolve() not in top_links:
          errors.append(f'{relative}: breadcrumb must link to repository home')
        related = re.split(r'^## Related Documents\s*$', text, flags=re.M)
        if len(related) != 2 or not list(links(related[1])):
          errors.append(f'{relative}: require Related Documents with a link')
      continue
    if source.name == 'README.md' and source.parent != root / 'docs':
      parent_index = source.parent.parent / 'README.md'
      registered = {local_target(root, parent_index, url) for url in links(parent_index.read_text(encoding='utf-8'))} if parent_index.exists() else set()
      if source.resolve() not in registered:
        errors.append(f'{relative}: missing category registration in parent README.md')
    if source.name != 'README.md':
      index = source.parent / 'README.md'
      if source.resolve() not in graph.get(index.resolve(), set()):
        # Traversal order does not guarantee the index has been processed yet.
        indexed = {local_target(root, index, url) for url in links(index.read_text(encoding='utf-8'))} if index.exists() else set()
        if source.resolve() not in indexed:
          errors.append(f'{relative}: missing registration in category README.md')
      if source.name != 'AGENTS.md':
        top_links = {local_target(root, source, url) for url in links('\n'.join(text.splitlines()[:5]))}
        if not {(root / 'docs/README.md').resolve(), index.resolve()} <= top_links:
          errors.append(f'{relative}: breadcrumb must link to docs hub and category index')
        related = re.split(r'^## Related Documents\s*$', text, flags=re.M)
        if len(related) != 2 or not list(links(related[1])):
          errors.append(f'{relative}: require Related Documents with a link')
  hub = (root / 'docs/README.md').resolve()
  reached, pending = set(), [hub]
  while pending:
    current = pending.pop()
    if current not in reached and current.is_relative_to(root / 'docs'):
      reached.add(current)
      pending.extend(graph.get(current, set()))
  for source in files:
    if source.is_relative_to(root / 'docs') and source.resolve() not in reached:
      errors.append(f'{source.relative_to(root)}: unreachable from documentation hub')
  return errors




def secret_path(name):
  """Identify credential filenames, allowing explicitly named example files."""
  base = Path(name).name
  if base.endswith('.example'):
    return False
  return (base == '.env' or base.startswith('.env.') or base.endswith('.env')
          or base in {'id_rsa', 'id_ed25519'}
          or any(fnmatch.fnmatchcase(base, pattern) for pattern in
                 ('*.pem', '*.key', '*.pfx', '*.p12', '*.id_rsa', '*.id_ed25519', '*.keystore')))


def check_secrets(root):
  tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root)
  return [f'Credential filename is tracked: {os.fsdecode(name)!r}'
          for name in tracked.split(b'\0') if name and secret_path(os.fsdecode(name))]


REQUIRED_FILES = (
  'README.md', 'LICENSE', 'SECURITY.md', 'CODE_OF_CONDUCT.md', 'CONTRIBUTING.md',
  'AGENTS.md', '.editorconfig', '.gitattributes', '.gitignore', 'docs/README.md',
)


def check_repository(root):
  errors = [f'Missing foundation file: {name}' for name in REQUIRED_FILES
            if not (root / name).is_file()]
  # Check repository shell entry points without changing their permissions.
  scripts = sorted((root / 'scripts').glob('*/*.sh'))
  scripts.append(root / '.githooks/commit-msg')
  for script in scripts:
    name = script.relative_to(root)
    if not script.is_file() or script.is_symlink():
      errors.append(f'{name}: shell entry point must be a regular file')
    elif not script.stat().st_mode & 0o111:
      errors.append(f'{name}: shell entry point must be executable')

  # This is a narrow literal-reference check, not a YAML or workflow validator.
  workflows = root / '.github/workflows'
  for workflow in sorted(list(workflows.glob('*.yml')) + list(workflows.glob('*.yaml'))):
    for number, line in enumerate(workflow.read_text(encoding='utf-8').splitlines(), 1):
      match = re.match(r"^\s*(?:-\s*)?uses:\s*['\"]?([^\s#'\"]+)", line)
      if match:
        action = match[1]
        if not action.startswith('./') and not re.fullmatch(r'[^@]+@[0-9a-fA-F]{40}', action):
          errors.append(f'{workflow.relative_to(root)}:{number}: external action or workflow must use a full commit SHA')
  return errors


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('check', choices=['links', 'docs', 'secrets', 'repository'])
  args = parser.parse_args()
  if sys.version_info < (3, 9):
    parser.error('Python 3.9 or newer is required')
  root = Path(__file__).resolve().parents[2]
  try:
    errors = {'links': check_links, 'docs': check_docs,
              'secrets': check_secrets, 'repository': check_repository}[args.check](root)
  except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as error:
    print(f'Check failed: {error}', file=sys.stderr)
    return 1
  for error in errors:
    print(error, file=sys.stderr)
  if errors:
    return 1
  print(f'{args.check.capitalize()} checks passed.')
  return 0


if __name__ == '__main__':
  sys.exit(main())
