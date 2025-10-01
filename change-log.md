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
