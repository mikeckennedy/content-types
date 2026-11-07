# Reverse lookup

So far the envelope has had a label and you wanted to know what was inside. Now flip it. A server has just told you what is inside, in the form of a `Content-Type` header, and you need to write a label. That is reverse lookup, and it is harder than it sounds.


# From a type to an extension

[guess_extension()](../reference/guess_extension.md#content_types.guess_extension) is the inverse of [get_content_type()](../reference/get_content_type.md#content_types.get_content_type). Give it a content type and it returns the canonical extension, with the dot, ready to append to a filename. [guess_all_extensions()](../reference/guess_all_extensions.md#content_types.guess_all_extensions) returns every extension known for that type, canonical first.

``` python
import content_types

content_types.guess_extension('application/pdf')  # '.pdf'
content_types.guess_extension('image/jpeg')  # '.jpg'
content_types.guess_all_extensions('image/jpeg')  # ['.jpg', '.jpeg', '.jpe']
content_types.guess_extension('image/jpeg', with_dot=False)  # 'jpg'
```

The classic use is naming a download when the URL gives you nothing to go on.

``` python
import httpx
from pathlib import Path

resp = httpx.get('https://example.com/download/item')
ext = content_types.guess_extension(resp.headers['content-type'])
if ext:
    Path(f'downloaded{ext}').write_bytes(resp.content)
```


# Why the reverse direction is the hard one

The forward table is one-to-one. Each of its 364 extensions maps to exactly one type. Run it backwards and it is one-to-many: those 364 extensions collapse onto 223 types, and 57 of those types have more than one extension pointing at them. `image/jpeg` is claimed by `.jpg`, `.jpeg`, and `.jpe`. Which one do you write on the label? Someone has to pick, and the pick has to be stable.

The rule is that the first extension listed for a type in [EXTENSION_TO_CONTENT_TYPE](../reference/EXTENSION_TO_CONTENT_TYPE.md#content_types.EXTENSION_TO_CONTENT_TYPE) wins, with a short list of deliberate overrides where the first-listed spelling is the one nobody uses any more: `text/html` gives `.html` not `.htm`, `image/tiff` gives `.tiff`, `video/mpeg` gives `.mpeg`, and `application/x-msdownload` gives `.exe` rather than `.dll`. Whatever the pick, `guess_extension(t)` is always equal to `guess_all_extensions(t)[0]`, and a test enforces it.

The standard library makes its own picks and orders its lists differently, so do not expect the two to agree. [Compared to mimetypes](compared-to-mimetypes.md) has the details.


# It reads headers as servers actually write them

Real `Content-Type` headers are messy. They carry parameters, they vary in case, and a surprising number of servers send spellings that were never registered. The reverse lookup takes all of that in stride.

- Case is ignored. `IMAGE/JPEG` resolves like `image/jpeg`.
- Parameters are stripped, so you can pass the raw header value. `text/html; charset=utf-8` resolves like `text/html`.
- Legacy and mistaken spellings resolve to the type this library uses. `text/json`, `image/jpg`, `audio/mp3`, `text/xml`, `application/javascript`, `application/x-yaml`, `application/x-zip-compressed`, and `application/x-gzip` all work. The complete alias list lives in the source as `_CONTENT_TYPE_ALIASES`, and tests check that every alias points at a real type and never shadows one.


# When it does not know

An unknown content type is not an error. [guess_extension()](../reference/guess_extension.md#content_types.guess_extension) returns `None` and [guess_all_extensions()](../reference/guess_all_extensions.md#content_types.guess_all_extensions) returns `[]`. Empty, whitespace-only, and parameter-only input all count as unknown. Passing `None` raises `TypeError`, matching the forward function.

``` python
content_types.guess_extension('application/x-nope')  # None
content_types.guess_all_extensions('application/x-nope')  # []
```

The `or` idiom is your friend here: `guess_extension(header) or '.bin'` gives you a usable label every time.


# The two catch-all types

`text/plain` and `application/octet-stream` are where extensions go when nothing more specific exists. `text/plain` has 32 extensions in the table and `application/octet-stream` has 24. Asked for the canonical pick, the library gives you `.txt` and `.bin`, which is as sensible as it gets. Asked for the full list, it gives you config files, pickles, object files, and database fragments all in one pile. If a server tells you `application/octet-stream`, the honest reading is that it does not know either, and any extension you write is a guess.
