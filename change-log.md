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
