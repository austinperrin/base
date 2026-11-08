"""Discover optional pinned linters without depending on runner image versions."""
import shutil
import subprocess


def pinned_tool(name, version_args, expected_line):
  path = shutil.which(name)
  if not path:
    return None
  try:
    result = subprocess.run([path, *version_args], capture_output=True, text=True,
                            timeout=10, check=False)
  except (OSError, subprocess.TimeoutExpired):
    return None
  if result.returncode == 0 and expected_line in result.stdout.splitlines():
    return path
  return None
