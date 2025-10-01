# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Development Commands and Workflow

### Building the Package
```bash
# Build wheel and source distribution
python -m build
```

### Code Quality and Formatting
```bash
# Run linting (configured for 120-char line length, single quotes, E/F rules)
ruff check .

# Format code (enforces single-quote style)  
ruff format .
```

### Installation and Testing
```bash
# Install in editable mode for development
pip install -e .

# Test the CLI tool
content-types example.jpg
content-types .webp
content-types --help  # May not be implemented

# Run comparison with Python's built-in mimetypes
python samples/compare_to_builtin.py
```

### Package Management
```bash
# Install via uv (recommended in README)
uv pip install content-types

# Install CLI globally with uv
uv tool install content-types
```

## High-level Architecture and Code Structure

### Core Data Structure
- **`EXTENSION_TO_CONTENT_TYPE`** dictionary in `content_types/__init__.py` contains ~225 file extension mappings
- Extensions are stored without the dot (e.g., `'jpg': 'image/jpeg'`)
- Provides more accurate and complete mappings than Python's built-in `mimetypes` module

### Main API Function  
```python
def get_content_type(filename_or_extension: str | Path, treat_as_binary: bool = True) -> str
```
- Accepts both string filenames and `pathlib.Path` objects
- Extracts extension from filename (handles complex cases like `archive.tar.gz`)
- Falls back to `application/octet-stream` (binary mode) or `text/plain` (text mode)
- Handles extensions with or without leading dot

### Convenience Constants
Pre-defined shortcuts for common types:
```python
webp, png, jpg, mp3, json, pdf, zip, xml, csv, md
```

### CLI Entry Point
- Defined in `pyproject.toml` as `content-types = "content_types:cli"`
- Simple usage: `content-types filename` outputs the MIME type
- Exits with usage message if no arguments provided

### Comparison Script
- `samples/compare_to_builtin.py` compares this library against Python's `mimetypes`
- Demonstrates 5 disagreements and 31 types not in built-in module
- Useful for validating improvements over standard library

## Key Technical Details

- **Python Version**: Requires Python 3.10+
- **Dependencies**: Zero runtime dependencies (pure Python)
- **Build System**: Hatchling backend
- **Code Style**: Single quotes enforced via Ruff formatter
- **Type Support**: Handles both `str` and `pathlib.Path` inputs  
- **Fallback Strategy**: `application/octet-stream` (binary) vs `text/plain` (text)
- **Package Structure**: Single module with everything in `__init__.py`
- **Testing**: No formal test suite detected; relies on comparison script for validation