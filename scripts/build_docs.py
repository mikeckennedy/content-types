#!/usr/bin/env python3
"""Build the docs and mirror the static site into the committed repo-root docs/ folder.

Great Docs writes its output to an ephemeral ``great-docs/_site`` directory (gitignored
and regenerated on every build). The project is hosted by committing the static site to
a repo-root ``docs/`` folder that the server serves via nginx, so this script runs the
build and then mirrors ``great-docs/_site`` -> ``docs`` (a full replace).

For this package the pyproject dir IS the git root, so REPO_ROOT == PKG_DIR.

Usage:
    python scripts/build_docs.py        # ideally with the project venv's interpreter
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
PKG_DIR = _SCRIPTS.parent  # dir with pyproject.toml + great-docs.yml
REPO_ROOT = PKG_DIR  # package lives at the git root here
SITE = PKG_DIR / 'great-docs' / '_site'
DEST = REPO_ROOT / 'docs'


def main() -> int:
    # Prefer the great-docs that ships next to the interpreter running this script
    # (i.e. the project venv); fall back to whatever is on PATH.
    great_docs = Path(sys.executable).with_name('great-docs')
    cmd = [str(great_docs) if great_docs.exists() else 'great-docs', 'build']
    if subprocess.run(cmd, cwd=PKG_DIR).returncode != 0:
        return 1

    if not SITE.is_dir():
        print(f'build output missing: {SITE}', file=sys.stderr)
        return 1

    if DEST.exists():
        shutil.rmtree(DEST)
    shutil.copytree(SITE, DEST)
    print(f'Mirrored -> {DEST} ({sum(1 for p in DEST.rglob("*") if p.is_file())} files)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
