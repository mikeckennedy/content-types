# Reverse lookup

The reverse functions turn a content type, or a raw `Content-Type` header, back into a file extension. This page covers what they accept, what they return on a miss, and how the canonical extension is chosen.


# From a content type to an extension

[guess_extension()](../reference/guess_extension.md#content_types.guess_extension) is the inverse of [get_content_type()](../reference/get_content_type.md#content_types.get_content_type). Give it a content type and it returns the canonical extension with a leading dot, ready to append to a filename. [guess_all_extensions()](../reference/guess_all_extensions.md#content_types.guess_all_extensions) returns every extension known for that type, canonical first.

``` python
import content_types

content_types.guess_extension('application/pdf')  # '.pdf'
content_types.guess_extension('image/jpeg')  # '.jpg'
content_types.guess_all_extensions('image/jpeg')  # ['.jpg', '.jpeg', '.jpe']
content_types.guess_extension('image/jpeg', with_dot=False)  # 'jpg'
```

The typical use is naming a download from an HTTP response.

``` python
import httpx
from pathlib import Path

resp = httpx.get('https://example.com/download/item')
ext = content_types.guess_extension(resp.headers['content-type'])
if ext:
    Path(f'downloaded{ext}').write_bytes(resp.content)
```


# What the lookup tolerates

- Case does not matter. `IMAGE/JPEG` resolves like `image/jpeg`.
- Parameters are ignored, so a raw `Content-Type` header value works. `text/html; charset=utf-8` resolves like `text/html`.
- Common non-canonical and legacy spellings resolve to the type this library uses. `text/json`, `image/jpg`, `audio/mp3`, `text/xml`, `application/javascript`, `application/x-yaml`, `application/x-zip-compressed`, and `application/x-gzip` all work. The full alias list is in the source as `_CONTENT_TYPE_ALIASES`.


# Unknown types

An unknown content type is not an error. [guess_extension()](../reference/guess_extension.md#content_types.guess_extension) returns `None` and [guess_all_extensions()](../reference/guess_all_extensions.md#content_types.guess_all_extensions) returns `[]`. Empty, whitespace-only, and parameter-only input count as unknown. Passing `None` raises `TypeError`, matching [get_content_type()](../reference/get_content_type.md#content_types.get_content_type).

``` python
content_types.guess_extension('application/x-nope')  # None
content_types.guess_all_extensions('application/x-nope')  # []
```


# Which extension is canonical

When several extensions share a type, the first one listed in [EXTENSION_TO_CONTENT_TYPE](../reference/EXTENSION_TO_CONTENT_TYPE.md#content_types.EXTENSION_TO_CONTENT_TYPE) wins, with a few deliberate overrides so the modern spelling comes first: `text/html` gives `.html` not `.htm`, `image/tiff` gives `.tiff`, `video/mpeg` gives `.mpeg`, and `application/x-msdownload` gives `.exe`. `guess_extension(t)` is always equal to `guess_all_extensions(t)[0]`.

The standard library `mimetypes` module can pick a different canonical extension and orders its lists differently, so do not expect the two to agree. See [Compared to mimetypes](compared-to-mimetypes.md).


# Two groups to know about

`text/plain` and `application/octet-stream` are the catch-all types, and each has many extensions. `guess_extension('text/plain')` returns `.txt` and `guess_extension('application/octet-stream')` returns `.bin`, which is sensible for both, but [guess_all_extensions()](../reference/guess_all_extensions.md#content_types.guess_all_extensions) on either returns a long list that includes config files, pickles, and object files. If you are naming a file from a header that says `application/octet-stream`, the extension is a guess at best.
