---
name: content-types
description: >
  A library to map file extensions to content types and vice versa. Use when writing Python code that uses the content_types package.
license: MIT
compatibility: Requires Python >=3.10.
---

# content-types

A library to map file extensions to content types and vice versa.

## Installation

```bash
pip install content-types
```

## API overview

### Lookup

The one entry point — map a filename, bare extension, Path, or URL to its MIME / content type.

- `get_content_type`: Given a filename (or just an extension), return the most specific,

### Mapping data

The underlying extension -> content-type table (364 entries; keys have no leading dot).

- `EXTENSION_TO_CONTENT_TYPE`: dict() -> new empty dictionary

### Shortcut constants

Precomputed content types for very common formats, exposed as module-level attributes.

- `webp`: str(object='') -> str
- `png`: str(object='') -> str
- `jpg`: str(object='') -> str
- `mp3`: str(object='') -> str
- `json`: str(object='') -> str
- `pdf`: str(object='') -> str
- `zip`: str(object='') -> str
- `xml`: str(object='') -> str
- `csv`: str(object='') -> str
- `md`: str(object='') -> str
- `parquet`: str(object='') -> str
- `ipynb`: str(object='') -> str
- `pkl`: str(object='') -> str
- `yaml`: str(object='') -> str
- `toml`: str(object='') -> str
- `sqlite`: str(object='') -> str

## Resources

- [Full documentation](https://mkennedy.codes/docs/content-types/)
- [llms.txt](llms.txt) — Indexed API reference for LLMs
- [llms-full.txt](llms-full.txt) — Comprehensive documentation for LLMs
- [Source code](https://github.com/mikeckennedy/content-types)
