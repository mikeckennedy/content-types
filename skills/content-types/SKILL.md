---
name: content-types
description: Maps a filename, bare extension, pathlib.Path, or URL to its MIME / content type by table lookup alone, never reading the file, and maps a content type or raw Content-Type header back to a file extension. Use when Python code needs a Content-Type header or S3 ContentType for a file it has not opened, names a download from a response header, gets application/octet-stream and must tell a miss from a real binary, chooses between treat_as_binary, fallback, and fallback=None, hits TypeError "filename cannot be None", would otherwise reach for the stdlib mimetypes module, or runs the content-types CLI.
license: MIT
compatibility: Python >=3.10, no runtime dependencies, pure Python.
---

# content-types

You know a filename, an S3 key, or a URL and need its MIME type without downloading or opening anything. `content_types.get_content_type()` returns the type string for the extension, or `application/octet-stream` when the extension is unknown. `guess_extension()` goes the other way, from a type or header value to an extension. Nothing here reads bytes. The import name is `content_types`; the distribution and CLI name is `content-types`.

## Install

```bash
uv add content-types        # or: pip install content-types
```

## Use

```python
import content_types

content_types.get_content_type('report.pdf')  # 'application/pdf'
content_types.get_content_type('https://cdn.x.com/a.mp3?v=3')  # 'audio/mpeg', query stripped
content_types.get_content_type('notes.xyz', fallback=None)  # None, so you can branch on a miss
content_types.guess_extension('text/html; charset=utf-8')  # '.html', params ignored
```

S3 upload: `ExtraArgs={'ContentType': content_types.get_content_type(key)}`. Download naming: `ext = content_types.guess_extension(resp.headers['content-type']) or '.bin'`.

## Rules

- Lookup only. The file does not need to exist and is never opened. For byte sniffing use another tool and fall through to it on `fallback=None`.
- Unknown extensions return `application/octet-stream`, not `None`, so a miss looks like a hit. Some real formats (`.bin`, `.pkl`, `.npy`, `.so`) also map to that type on purpose. Pass `fallback=None` when you need to know.
- `fallback` beats `treat_as_binary`. Omitting `fallback` and passing `fallback=None` are different: the default is a private sentinel, so omitting it keeps the `application/octet-stream` / `text/plain` behaviour.
- Typing: the default call and a string `fallback` return `str`; only `fallback=None` returns `Optional[str]`. Overloads make this precise, so do not add needless `assert x is not None` after a default call.
- The last dot-segment wins. `archive.tar.gz` is `application/gzip`; there is no `tar.gz` entry. `.env` and `.gitignore` are known and return `text/plain`. `Makefile`, `''`, and a URL with no file part are misses.
- Matching is case-insensitive both directions. `?query` and `#fragment` are stripped from URLs first.
- `None` as the input raises `TypeError` in every function. Unknown values do not raise anywhere: forward gives the fallback, `guess_extension` gives `None`, `guess_all_extensions` gives `[]`.
- Reverse lookup accepts raw header values with parameters and legacy spellings (`text/json`, `image/jpg`, `audio/mp3`, `text/xml`, `application/javascript`, `application/x-yaml`, `application/x-zip-compressed`, `application/x-gzip`). Canonical picks differ from stdlib: `text/html` gives `.html`, `image/jpeg` gives `.jpg`, `image/tiff` gives `.tiff`. `guess_extension(t) == guess_all_extensions(t)[0]` always.
- The answers are deliberately modern and differ from `mimetypes`: `.xml` is `application/xml`, `.js` is `text/javascript`, `.yaml` / `.yml` are `application/yaml` (RFC 9512), `.md` is `text/markdown`. Do not "correct" them back.
- The API is not `mimetypes`. There is no `guess_type()`; the forward call is `get_content_type()` and it returns one string, not a `(type, encoding)` tuple.
- `EXTENSION_TO_CONTENT_TYPE` keys have no leading dot (`['jpg']`, never `['.jpg']`). It is a plain dict and may be extended at startup; the reverse map is built once on first reverse call and cached, so add entries before that.
- Prefer `import content_types` and attribute access. `from content_types import json, csv, zip` shadows a stdlib module, a stdlib module, and a builtin.
- Second calls are plain dict reads. There is no state, no config, and no environment variable.

## Decision table

| Need | Use |
| --- | --- |
| Header or S3 ContentType for a name you have | `get_content_type(name)` |
| Know whether the extension is unknown | `get_content_type(name, fallback=None)` and test for `None` |
| Text default instead of binary for misses | `get_content_type(name, treat_as_binary=False)` |
| Your own placeholder for misses | `get_content_type(name, fallback='application/x-acme')` |
| Extension for a `Content-Type` header value | `guess_extension(header)` then `or` a default |
| Every extension for a type, canonical first | `guess_all_extensions(content_type)` |
| Bare extension without the dot | `with_dot=False` on either reverse function |
| Yes/no membership with no fallback | `ext in EXTENSION_TO_CONTENT_TYPE` (lowercase, no dot) |
| Common type without a call | `content_types.json`, `.pdf`, `.png`, `.parquet`, ... |
| Shell one-off | `content-types photo.jpg` |

## API

- `get_content_type(filename_or_extension: str | Path, treat_as_binary: bool = True, fallback: str | None = <omitted>) -> str` (`Optional[str]` only with `fallback=None`). Raises `TypeError` on `None` input. Forward lookup; this is the one you want most of the time.
- `guess_extension(content_type: str, with_dot: bool = True) -> Optional[str]`. Raises `TypeError` on `None`. Returns the canonical extension or `None`.
- `guess_all_extensions(content_type: str, with_dot: bool = True) -> list[str]`. Raises `TypeError` on `None`. Returns all extensions canonical first, or `[]`.
- `EXTENSION_TO_CONTENT_TYPE: dict[str, str]`. 364 bare-extension keys. The single source of truth for both directions.
- Constants `webp png jpg mp3 json pdf zip xml csv md parquet ipynb pkl yaml toml sqlite: str`. Plain strings computed at import.
- `cli() -> None`. Entry point for the `content-types` script. One positional argument, forward lookup only; `-h` / `--help` and `--version` exit 0; no argument prints usage and exits 1; unknown extension prints `application/octet-stream` and exits 0.

## Worked example

```python
>>> content_types.get_content_type('model.pkl')
'application/octet-stream'      # a hit: .pkl really is octet-stream
>>> content_types.get_content_type('model.pkl', fallback=None)
'application/octet-stream'      # still a string, so the extension is known
>>> content_types.get_content_type('model.weights', fallback=None)
None                            # a miss: not in the table
>>> content_types.guess_all_extensions('application/octet-stream')[:3]
['.bin', '.a', '.so']           # reverse of a catch-all type is a guess at best
```

Fix order on a miss: check the spelling and case of the name, check `EXTENSION_TO_CONTENT_TYPE` for the bare key, add the entry at startup if it is private to your app, and open an issue at the repo if it is a format others would expect.

## Resources

- Docs: <https://mkennedy.codes/docs/content-types/>
- Getting started: <https://mkennedy.codes/docs/content-types/user-guide/getting-started.html>
- Unknown extensions and fallbacks: <https://mkennedy.codes/docs/content-types/user-guide/unknown-extensions.html>
- Reverse lookup: <https://mkennedy.codes/docs/content-types/user-guide/reverse-lookup.html>
- Compared to mimetypes: <https://mkennedy.codes/docs/content-types/user-guide/compared-to-mimetypes.html>
- API reference: <https://mkennedy.codes/docs/content-types/reference/index.html>
- llms.txt: <https://mkennedy.codes/docs/content-types/llms.txt>
- llms-full.txt: <https://mkennedy.codes/docs/content-types/llms-full.txt>
- Source: <https://github.com/mikeckennedy/content-types>
