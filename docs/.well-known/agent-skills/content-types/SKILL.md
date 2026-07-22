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

### Forward lookup

Map a filename, bare extension, Path, or URL to its MIME / content type.

- `get_content_type`: Return the most specific, commonly accepted MIME type for a filename or extension

### Reverse lookup

Map a MIME / content type back to its file extension(s) — the inverse of get_content_type.

- `guess_extension`: Return the canonical file extension for a MIME / content type
- `guess_all_extensions`: Return every known file extension for a MIME / content type, canonical first

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

## End-to-end wiring

The core use case: you know a filename (often for a remote/S3 object you don't want to download) and need its content type — and sometimes the reverse, turning an HTTP `Content-Type` header back into a file extension. The library never opens or sniffs file bytes; everything is extension lookup.

```python
from pathlib import Path
import boto3
import content_types

s3 = boto3.client('s3')

# Upload with the correct Content-Type (S3 defaults to binary/octet-stream otherwise)
local = Path('reports/summary.pdf')
s3.upload_file(
    str(local), 'my-bucket', f'reports/{local.name}',
    ExtraArgs={'ContentType': content_types.get_content_type(local)},  # 'application/pdf'
)

# Reverse: pick a filename extension from a response's Content-Type header
import httpx
resp = httpx.get('https://example.com/download/item')
ext = content_types.guess_extension(resp.headers['content-type'])  # e.g. '.png' — params like '; charset=...' are stripped
if ext:
    Path(f'downloaded{ext}').write_bytes(resp.content)
```

## It is not `mimetypes` — the API and the answers differ

Do not guess this API from the standard library `mimetypes` module. The forward function is `get_content_type()` (not `guess_type()`, and it returns the type string alone, not a `(type, encoding)` tuple). `guess_extension()`/`guess_all_extensions()` exist in both, but this library's versions accept full header values with parameters (`'text/html; charset=utf-8'`), resolve legacy alias spellings (`text/json`, `image/jpg`, `audio/mp3`, `application/x-zip-compressed`, `text/xml`, `application/javascript` all resolve to their canonical types), and return the canonical extension first — `text/html` → `.html` (stdlib often says `.htm`), `image/jpeg` → `.jpg`.

The answers are deliberately modernized too: `.xml` → `application/xml`, `.js` → `text/javascript`, `.yaml`/`.yml` → `application/yaml` (RFC 9512, not the legacy `text/yaml`), `.md` → `text/markdown`, plus ~264 extensions the stdlib is missing entirely (`.webp`, `.parquet`, `.ipynb`, `.woff2`, `.heic`, `.mkv`, ...).

## Input shapes and edge cases for `get_content_type()`

All of these work: a filename (`'photo.jpg'`), a full path (`'images/photo.jpg'`), a bare extension (`'jpg'` or `'.jpg'`), a `pathlib.Path`, or a URL — query strings (`?...`) and fragments (`#...`) are stripped first. Matching is case-insensitive.

Compound extensions use the **last** segment only: `archive.tar.gz` → `application/gzip` (there is no special `tar.gz` handling). Extension-less names (`Makefile`, `.gitignore`, `''`) are unknown and get the fallback.

## Unknown extensions: `treat_as_binary` vs `fallback`

Three distinct behaviors, and `fallback` wins over `treat_as_binary` when both are given:

```python
content_types.get_content_type('x.xyz')                          # 'application/octet-stream' (default)
content_types.get_content_type('x.xyz', treat_as_binary=False)   # 'text/plain'
content_types.get_content_type('x.xyz', fallback='application/x-custom')  # your placeholder
content_types.get_content_type('x.xyz', fallback=None)           # None — branch on a miss
```

`fallback=None` is meaningful, not the default: the parameter defaults to a private sentinel, so omitting `fallback` keeps the `treat_as_binary` behavior while an explicit `None` returns `None` for unknowns. Passing `None` as the *filename* raises `TypeError`; so does passing `None` to the reverse-lookup functions (which signal unknown types with `None` / `[]` instead).

## Keys in the mapping table have no leading dot

`EXTENSION_TO_CONTENT_TYPE` keys are bare lowercase extensions: `EXTENSION_TO_CONTENT_TYPE['jpg']`, never `['.jpg']`. By contrast, `guess_extension()`/`guess_all_extensions()` return extensions **with** the dot by default (`'.pdf'`) — pass `with_dot=False` for bare ones.

## Shortcut constants are plain strings

Sixteen precomputed module-level constants (`webp`, `png`, `jpg`, `mp3`, `json`, `pdf`, `zip`, `xml`, `csv`, `md`, `parquet`, `ipynb`, `pkl`, `yaml`, `toml`, `sqlite`) are just the looked-up strings, ready for headers: `{'Content-Type': content_types.json}`. Watch the names when using `from content_types import ...` — `json`, `zip`, and `csv` shadow the stdlib module / builtin; prefer `import content_types` and attribute access.

## CLI

The package installs a `content-types` console script that does forward lookup only:

```bash
$ content-types photo.jpg
image/jpeg
$ content-types .webp
image/webp
```

## Fetching the docs as Markdown

Every page on the documentation site has a plain-Markdown twin: swap the `.html` extension for `.md` to get token-efficient source without the site chrome. For example https://mkennedy.codes/docs/content-types/reference/get_content_type.html is also available at https://mkennedy.codes/docs/content-types/reference/get_content_type.md. Prefer the `.md` form when reading these docs programmatically.


## Resources

- [Full documentation](https://mkennedy.codes/docs/content-types/)
- [llms.txt](llms.txt) — Indexed API reference for LLMs
- [llms-full.txt](llms-full.txt) — Comprehensive documentation for LLMs
- [Source code](https://github.com/mikeckennedy/content-types)
