# CLAUDE.md

A field guide for anyone building on or inside this repository, human or agent. It tells you what the package is for, how it is put together, how to run the checks, and the handful of things that will bite you if nobody warns you.

## What this thing is

`content-types` answers one question: what is the MIME type of a file whose name you know but whose bytes you may never see. It does that by lookup only. It never opens, reads, or sniffs a file, and that is the design constraint behind every decision below. The canonical use is an object in S3 or a URL you have not fetched, where downloading the thing just to inspect its header bytes would be slow and silly.

It aims to be more complete and more correct than the standard library `mimetypes` module: 364 extensions against a built-in table that ranges from 142 entries on Python 3.10 to about 210 on 3.15, and modern answers such as `.xml` -> `application/xml` where the stdlib still says `text/xml`. It ships as an importable library and as a `content-types` CLI. Zero runtime dependencies, pure Python, Python 3.10 and up.

## Commands

`pytest` and `ruff` are **not** declared dependencies. Run them through `uv`, which provides them on the fly.

```bash
# Tests (75 tests)
uv run --with pytest pytest

# A single test by node id, or by keyword
uv run --with pytest pytest tests/test_content_types.py::TestGetContentType::test_case_insensitive
uv run --with pytest pytest -k case_insensitive

# Lint and format (config in ruff.toml)
uvx ruff check .
uvx ruff format .

# Type check (the package is typed and must stay clean)
ty check content_types

# Build wheel + sdist (hatchling backend)
uv build

# Run the CLI / the mimetypes comparison script
uv run content-types example.jpg
uv run python samples/compare_to_builtin.py
```

## Architecture

Everything lives in one module: [content_types/__init__.py](content_types/__init__.py). There is no internal package structure to learn. The design is intentionally flat, and the whole file reads top to bottom in one sitting: the table, the reverse-lookup helpers, the forward function, the constants, the CLI.

- **`EXTENSION_TO_CONTENT_TYPE`** is the single source of truth, a `dict[str, str]` of 364 entries. **Keys are extensions with no leading dot** (`'jpg'`, not `'.jpg'`), and a test enforces it. Entries are grouped by category with comments, and within a group the canonical extension for a type comes first, because the reverse lookup depends on that ordering.
- **`get_content_type(filename_or_extension, treat_as_binary=True, fallback=_UNSET)`** is the forward lookup. It accepts a `str` or a `pathlib.Path` (the final path component is used, so `Path('.env')` and `'.env'` agree), strips URL query strings (`?...`) and fragments (`#...`), takes the **last** dot-segment as the extension (`archive.tar.gz` -> `gz`, never `tar.gz`), lowercases it, and reads the table. Unknown extensions fall back to `application/octet-stream` or, with `treat_as_binary=False`, `text/plain`. An explicit `fallback` (including `fallback=None`) outranks both. The default is a private sentinel, `_UNSET`, so an omitted argument and an explicit `None` can be told apart. Overloads keep the return type `str` unless `fallback=None` is passed. `None` as input raises `TypeError`.
- **`guess_extension(content_type, with_dot=True)` / `guess_all_extensions(content_type, with_dot=True)`** run the table backwards. The inverted map is built lazily by `_reverse_map()` and cached with `functools.cache`, so callers who only do forward lookups never pay for it. Two small tables steer the result: `_CANONICAL_OVERRIDES` promotes the modern spelling where the first-listed extension is a relic (`.html` over `.htm`), and `_CONTENT_TYPE_ALIASES` accepts legacy MIME spellings (`text/json`, `image/jpg`, `application/x-gzip`) on reverse lookup only. The forward table stays pure. Unknown types return `None` and `[]`; `None` input raises `TypeError`.
- **Shortcut constants** (`webp`, `png`, `jpg`, `mp3`, `json`, `pdf`, `zip`, `xml`, `csv`, `md`, plus the data-science set `parquet`, `ipynb`, `pkl`, `yaml`, `toml`, `sqlite`) are module-level strings computed at import time by calling `get_content_type`. Yes, `json`, `zip`, and `csv` shadow a stdlib module or builtin inside this module. That is deliberate and confined to attribute access on the package.
- **`cli()`** is wired as the `content-types` entry point in [pyproject.toml](pyproject.toml). One positional argument, forward lookup only. No argument prints usage and exits 1; `-h` / `--help` print usage and `--version` prints the version, both exit 0.

**Version gotcha:** `__version__ = version('content-types')` reads from *installed* distribution metadata via `importlib.metadata`, so importing the package requires it to be installed (editable). `uv run ...` handles this automatically. A bare `python -c "import content_types"` against a clean checkout fails with `PackageNotFoundError`, and the first time it happens to you it will look like something far worse.

## The invariants the tests defend

The reverse lookup is where the complexity hides, so most of the property tests live there. If you touch the table or the helper dicts, these are the promises you are keeping:

- Every content type in the table has a canonical extension that maps forward to that same type.
- `guess_extension(t)` always equals `guess_all_extensions(t)[0]`.
- Every alias in `_CONTENT_TYPE_ALIASES` points at a type that really exists in the table, and no alias key is itself a canonical type, so an alias can never shadow a real answer.
- Every key in the table has no leading dot.
- `_UNSET` has a stable `repr`, so generated docs and `llms-full.txt` never embed a memory address.

## Conventions

- Ruff enforces **single quotes**, 120-char lines, rules `E`/`F`/`I`, and max complexity 10. Match the existing single-quote style, including inside fenced Python in Markdown, because `ruff format` checks those fences too.
- **Nullable types:** always write `Optional[X]` (import from `typing`), never `X | None`. `str | Path` is a true union of two peer types, but `X | None` conflates "a value" with "absence of one," which `Optional[X]` states directly. Keep real unions as `|`; use `Optional` only for the nullable case.
- **Adding an extension:** add the key (no dot) to `EXTENSION_TO_CONTENT_TYPE` in the appropriate category block, and add a spot-test assertion in [tests/test_content_types.py](tests/test_content_types.py). If the type already has other extensions, put the new one after the canonical spelling, not before it. If it is a very common type, also add a module-level shortcut constant, an attribute docstring with an example, and an assertion in `TestShortcutConstants`.
- **Docstrings** are Google style (`Args:` / `Returns:` / `Raises:` / `Example:`) and every public name has an `Example:` block with a fenced Python snippet. Great Docs renders those on the reference pages and copies them into `llms-full.txt`, so they are the cheapest way to make the reference useful to both humans and agents.
- **Markdown prose is never hard-wrapped.** One paragraph per physical line, in every `.md` and `.qmd` file in the repo.

## Docs

The site at [mkennedy.codes/docs/content-types](https://mkennedy.codes/docs/content-types/) is built with [Great Docs](https://github.com/posit-dev/great-docs) and configured in [great-docs.yml](great-docs.yml).

- **Landing page** is the README, rendered as-is.
- **User guide** is `user_guide/*.qmd`. Numeric prefixes (`01-`, `02-`) set the order and are stripped from the published URLs, so `01-getting-started.qmd` becomes `user-guide/getting-started.html`. Each page starts with a one-line intro paragraph before its first heading; Great Docs only emits the page title into `llms-full.txt` when the body does not begin with a heading.
- **Agent skill** is hand-written in `skills/content-types/SKILL.md` and copied verbatim to `skill.md`, `.well-known/agent-skills/content-types/SKILL.md`, and `.well-known/skills/default/SKILL.md`. Because it is served from several paths, every link in it must be an absolute URL. It is a cheat sheet, not a manual; keep it under about 100 lines.
- **API reference** is generated with `dynamic: false` on purpose. Dynamic introspection cannot see the attribute docstrings on the table and the constants and reports the builtin `dict` / `str` docstrings instead. `llms-full.txt` imports the package regardless of this setting, which is why the build needs the package installed.
- **Build** with `python scripts/build_docs.py` from the project venv (`uv pip install -e ".[dev]"` first). It runs `great-docs build`, mirrors `great-docs/_site/` into the committed `docs/` folder, and fails if `llms.txt`, `llms-full.txt`, `skill.md`, or the `.well-known` files are missing, because Great Docs reports success even when the package failed to import. `great-docs/` is gitignored and regenerated on every build; `docs/` is committed and served by nginx under `/docs/content-types/`. Preview the committed site exactly as hosted with `python scripts/serve_docs.py`.
- The hosted changelog page is generated from GitHub Releases, not from `change-log.md`, so a release is not fully published until the GitHub Release exists.

## Releasing

Version is hardcoded in [pyproject.toml](pyproject.toml) (`[project].version`) and surfaces at runtime via the metadata lookup above. The flow (see the matching `.cursor/commands/`):

1. Move the `[Unreleased]` entries in [change-log.md](change-log.md) into a new `[X.Y.Z] - YYYY-MM-DD` section (Keep a Changelog format, SemVer `M.m.b`). The change log is the authoritative record.
2. Bump `version` in `pyproject.toml` to match.
3. Tag `vX.Y.Z` and push the tag to `origin`.

Before any of that, check whether the current version is already on PyPI. If it is, new changelog entries go under `[Unreleased]`, not into the released section.
