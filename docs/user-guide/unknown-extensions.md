# Unknown extensions

A lookup that misses still returns a string by default. This page explains how to recognise a miss, the three ways to handle one, and how to extend the table.


# How to read the result

[get_content_type()](../reference/get_content_type.md#content_types.get_content_type) always returns a string unless you ask it not to. For a known extension the string is the content type. For an unknown extension it is a fallback, and by default that fallback is `application/octet-stream`.

``` python
import content_types

content_types.get_content_type('data.parquet')  # 'application/vnd.apache.parquet'
content_types.get_content_type('notes.xyz')  # 'application/octet-stream'
content_types.get_content_type('Makefile')  # 'application/octet-stream'
```

`application/octet-stream` is the correct generic type for "some bytes" and it is what S3 and most web servers use when they do not know better. The catch is that a few real extensions also map to it on purpose, among them `.bin`, `.pkl`, `.npy`, `.so`, and `.exe` style binaries, so you cannot tell a miss from a hit by looking at the return value alone.


# Three ways to handle a miss

**Ask for `text/plain` instead.** If the files you handle are mostly text, `treat_as_binary=False` changes the default fallback.

``` python
content_types.get_content_type('notes.xyz', treat_as_binary=False)  # 'text/plain'
```

**Supply your own fallback.** Pass any string as `fallback` and it is returned for every unknown extension. It takes precedence over `treat_as_binary`. Known extensions are unaffected.

``` python
content_types.get_content_type('notes.xyz', fallback='application/x-acme')  # 'application/x-acme'
content_types.get_content_type('photo.jpg', fallback='application/x-acme')  # 'image/jpeg'
```

**Branch on the miss.** Pass `fallback=None` to get `None` back for unknowns, then decide what to do yourself. This is the one to use when a miss should change program flow, for example to sniff the bytes with another tool or to reject the upload.

``` python
content_type = content_types.get_content_type(name, fallback=None)
if content_type is None:
    content_type = sniff_with_python_magic(path)
```

Omitting `fallback` and passing `fallback=None` are different. Omitting it keeps the historical default. The parameter defaults to a private sentinel so the two cases can be told apart.


# Checking the table directly

If you only need a yes or no, read the table. Keys are bare lowercase extensions with no leading dot.

``` python
ext = 'parquet'
ext in content_types.EXTENSION_TO_CONTENT_TYPE  # True
```


# Adding your own extensions

The table is a plain `dict` and the lookup reads it on every call, so a process-local addition takes effect immediately. Keys must be lowercase and have no leading dot.

``` python
content_types.EXTENSION_TO_CONTENT_TYPE['acme'] = 'application/x-acme'
content_types.get_content_type('report.acme')  # 'application/x-acme'
```

Do this at startup, not per request, and keep in mind that the reverse lookup caches its view of the table on first use. If you need [guess_extension()](../reference/guess_extension.md#content_types.guess_extension) to see your additions, add them before the first reverse call.

If the extension is a real, widely used format that other people would expect to work, please [open an issue](https://github.com/mikeckennedy/content-types/issues) or send a pull request so it ends up in the table for everyone.


# Things that are not misses

- `None` as the filename raises `TypeError`. That is a programming error, not an unknown extension.
- An empty string, a bare name with no dot, and a URL with no file component all count as unknown and get the fallback.
- `archive.tar.gz` is not a miss. It resolves on the last segment and returns `application/gzip`.
