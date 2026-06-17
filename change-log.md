# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
-

### Changed
-

### Deprecated
-

### Removed
-

### Fixed
-

### Security
-

---

## [0.5.7] - 2026-06-17

### Added
- `guess_extension(content_type, with_dot=True)` — reverse lookup from a MIME type to its canonical file extension (e.g. `application/pdf` → `.pdf`), the inverse of `get_content_type()`. Case-insensitive, and MIME parameters on a `Content-Type` header are ignored (`text/html; charset=utf-8` → `.html`). Common non-canonical / legacy spellings also resolve (e.g. `text/json` → `.json`, `image/jpg` → `.jpg`, `application/x-zip-compressed` → `.zip`). Unknown types return `None`. (#9)
- `guess_all_extensions(content_type, with_dot=True)` — returns every known extension for a MIME type, canonical first (e.g. `image/jpeg` → `['.jpg', '.jpeg', '.jpe']`); unknown types return `[]`. Same case-insensitivity, parameter-stripping, and alias handling as `guess_extension()`. (#9)
- Files: `content_types/__init__.py`, `tests/test_content_types.py`, `README.md`, `great-docs.yml`, `docs/`

### Changed
- `get_content_type()` now distinguishes an omitted `fallback` from an explicit `fallback=None`. Passing `fallback=None` returns `None` for unknown extensions (handy when you want to branch on a miss rather than receive a placeholder type), while omitting `fallback` is unchanged and still returns `application/octet-stream` (or `text/plain` with `treat_as_binary=False`) — so existing callers are unaffected. The default keyword switched from `None` to a private sentinel to tell the two cases apart, and the return type widened to `Optional[str]`. (#8)
- Files: `content_types/__init__.py`, `tests/test_content_types.py`, `README.md`

---

## [0.4.0] - 2026-06-10

### Added
- `fallback` parameter on `get_content_type()` to override the default MIME type returned for unknown extensions — pass any string and it will be returned in place of `application/octet-stream` / `text/plain` (#8)
- URL support: `get_content_type()` now handles query strings and URL fragments
- MIME types for `.sas` (`text/x-sas`) and `.sql` (`application/sql`) extensions (#5)
- Comprehensive test suite (35 tests) covering integration, spot tests, and negative conditions
- Documentation site built with [Great Docs](https://github.com/posit-dev/great-docs) and published at <https://mkennedy.codes/docs/content-types/> — auto-generated API reference plus a README-driven landing page. Built locally with `scripts/build_docs.py` and served from the committed `docs/` folder (`scripts/serve_docs.py` previews it under the production subpath).
- Files: `content_types/__init__.py`, `tests/test_content_types.py`, `tests/__init__.py`, `pytest.ini`, `great-docs.yml`, `scripts/build_docs.py`, `scripts/serve_docs.py`, `pyproject.toml`, `docs/`

### Changed
- `get_content_type()` now raises `TypeError` (instead of a bare `Exception`) when called with `None`. The message is unchanged, so existing `except Exception` handlers keep working.
- Modernized type hints (`dict[str, str]`, `Optional[str]`) and rewrote the `get_content_type()` / `cli()` docstrings in Google style (Args/Returns/Raises) for a cleaner generated API reference.
- `.yaml`, `.yml`, and `.kubeconfig` now map to `application/yaml` (RFC 9512, registered 2024) instead of the legacy `text/yaml`. The `content_types.yaml` shortcut constant updates to match.
- Added the `Typing :: Typed` trove classifier to advertise the existing PEP 561 `py.typed` marker on PyPI; added a test asserting the marker ships with the package.
- Dynamic version metadata: package now pulls `__version__` from distribution metadata.
- The sdist now contains only the package, change log, readme, and license — previously it bundled every git-tracked file (the built `docs/` site, `tests/`, `scripts/`, editor config, etc.). Wheels were already minimal. (`[tool.hatch.build.targets.sdist]` in `pyproject.toml`)
- Files: `content_types/__init__.py`, `pyproject.toml`, `README.md`, `tests/test_content_types.py`

### Fixed
- `.ass` (Advanced SubStation Alpha subtitles) now maps to `text/x-ssa` — matching its sibling `.ssa` — instead of the incorrect `audio/aac`. `.rst` (reStructuredText, value unchanged at `text/x-rst`) moved out of the audio block into the documentation block.
- Docstring example for `get_content_type("script.js")` now shows `'text/javascript'` (the actual return value) instead of the outdated `'application/javascript'`
- Files: `content_types/__init__.py`

---

## [0.3.0] - 2025-10-01

### Added
- 137 new file extensions across 17 categories, expanding format recognition capabilities
- Comprehensive support for data-science MIME types (e.g., `application/vnd.pandas`, `application/x-ipynb+json`)
- Project now supports 360+ file formats
- Warp Project Summary / Index document for contributors and users
- Files: `content_types/__init__.py`, `WARP.md`

### Changed
- Implemented alphabetical sorting of output listings for better navigation
- Enhanced README to highlight 360+ supported file formats
- Improved docstrings throughout codebase for clarity
- Files: `content_types/__init__.py`, `README.md`

### Fixed
- Corrected CLI help text instructions for clearer usage guidance
- Adjusted code indentation for better visual consistency
- Files: `content_types/__init__.py`

---

## [0.2.3] - 2025-02-01

### Changed
- Changed `.js` back to `text/javascript`
- Added a few new content types
- Files: `content_types/__init__.py`

### Added
- Added comparison to builtin mimetypes
- Files: `samples/compare_to_builtin.py`

---

## [0.2.2] - 2025-01-31

### Added
- Added `py.typed` file to suppress mypy typing warnings (Thanks @sanders41)
- Files: `content_types/py.typed`

### Changed
- Now available on PyPI

---

## [0.2.1] - 2025-01-31

### Added
- Many more file extensions as known types
- Files: `content_types/__init__.py`

---

## [0.2.0] - 2025-01-31

### Added
- Initial public release
- Files: `content_types/__init__.py`, `pyproject.toml`, `README.md`

[Unreleased]: https://github.com/mikeckennedy/content-types/compare/v0.5.7...HEAD
[0.5.7]: https://github.com/mikeckennedy/content-types/compare/v0.4.0...v0.5.7
[0.4.0]: https://github.com/mikeckennedy/content-types/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/mikeckennedy/content-types/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/mikeckennedy/content-types/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/mikeckennedy/content-types/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/mikeckennedy/content-types/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/mikeckennedy/content-types/releases/tag/v0.2.0

---

## Template for Future Entries

<!--
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features or capabilities
- Files: `path/to/new/file.ext`, `another/file.ext`

### Changed
- Modifications to existing functionality
- Files: `path/to/modified/file.ext` (summary if many files)

### Deprecated
- Features that will be removed in future versions
- Files affected: `path/to/deprecated/file.ext`

### Removed
- Features or files that were deleted
- Files: `path/to/removed/file.ext`

### Fixed
- Bug fixes and corrections
- Files: `path/to/fixed/file.ext`

### Security
- Security patches or vulnerability fixes
- Files: `path/to/security/file.ext`

### Notes
- Additional context or important information
- Major dependencies updated
- Breaking changes explanation
-->
