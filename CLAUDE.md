# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`content-types` maps a file extension to its MIME / content type by lookup only — it never opens, reads, or sniffs the file's bytes (the use case is knowing a filename for a remote/S3 object you don't want to download). It aims to be more complete and more correct than the standard library `mimetypes` module (364 extensions vs. ~100, and modern/corrected types like `.xml` → `application/xml`). It ships as both an importable library and a `content-types` CLI. Zero runtime dependencies, pure Python, requires Python 3.10+.

## Commands

`pytest` and `ruff` are **not** declared dependencies, so run them through `uv` which provides them on the fly:

```bash
# Tests (35 tests)
uv run --with pytest pytest

# A single test by node id, or by keyword
uv run --with pytest pytest tests/test_content_types.py::TestGetContentType::test_case_insensitive
uv run --with pytest pytest -k case_insensitive

# Lint and format (config in ruff.toml)
uvx ruff check .
uvx ruff format .

# Build wheel + sdist (hatchling backend)
uv build

# Run the CLI / the mimetypes comparison script
uv run content-types example.jpg
uv run python samples/compare_to_builtin.py
```

## Architecture

Everything lives in one module: [content_types/__init__.py](content_types/__init__.py). There is no internal package structure to learn — the design is intentionally flat.

- **`EXTENSION_TO_CONTENT_TYPE`** — the single source of truth: a `dict[str, str]` of 364 entries. **Keys are extensions with no leading dot** (`'jpg'`, not `'.jpg'`); a test enforces this. Entries are grouped by category with comments.
- **`get_content_type(filename_or_extension, treat_as_binary=True)`** — the only function. It accepts a `str` or `pathlib.Path`, strips URL query strings (`?...`) and fragments (`#...`), takes the **last** dot-segment as the extension (so `archive.tar.gz` → `gz`, not `tar.gz`), lowercases it, and looks it up. Unknown extensions fall back to `application/octet-stream` (binary) or, when `treat_as_binary=False`, `text/plain`. `None` raises.
- **Shortcut constants** (`webp`, `png`, `jpg`, `mp3`, `json`, `pdf`, `zip`, `xml`, `csv`, `md`, plus data-science ones `parquet`, `ipynb`, `pkl`, `yaml`, `toml`, `sqlite`) are module-level strings computed at import time by calling `get_content_type`.
- **`cli()`** — wired as the `content-types` entry point in [pyproject.toml](pyproject.toml). Prints the looked-up type, or a usage message and `exit(1)` if given no argument.

**Version gotcha:** `__version__ = version('content-types')` reads from *installed* distribution metadata via `importlib.metadata`, so importing the package requires it to be installed (editable). `uv run ...` handles this automatically; a bare `python -c "import content_types"` against a clean checkout fails with `PackageNotFoundError`.

## Conventions

- Ruff enforces **single quotes**, 120-char lines, rules `E`/`F`/`I`, and max complexity 10. Match the existing single-quote style.
- **Nullable types:** always write `Optional[X]` (import from `typing`), never `X | None`. `str | Path` is a true union of two peer types, but `X | None` conflates "a value" with "absence of one," which `Optional[X]` states directly. Keep real unions as `|`; use `Optional` only for the nullable case.
- **Adding an extension:** add the key (no dot) to `EXTENSION_TO_CONTENT_TYPE` in the appropriate category block, and add a spot-test assertion in [tests/test_content_types.py](tests/test_content_types.py). If it's a very common type, also add a module-level shortcut constant and a corresponding assertion in `TestShortcutConstants`.

## Releasing

Version is hardcoded in [pyproject.toml](pyproject.toml) (`[project].version`) and surfaces at runtime via the metadata lookup above. The flow (see the matching `.cursor/commands/`):

1. Move the `[Unreleased]` entries in [change-log.md](change-log.md) into a new `[X.Y.Z] - YYYY-MM-DD` section (Keep a Changelog format, SemVer `M.m.b`). The change log is the authoritative record.
2. Bump `version` in `pyproject.toml` to match.
3. Tag `vX.Y.Z` and push the tag to `origin`.
