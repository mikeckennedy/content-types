# Compared to mimetypes

This page explains how the lookup works under the hood, how its answers differ from the standard library `mimetypes` module, and when a byte-sniffing library is the better tool.


# How the lookup works

Everything is one dictionary, [EXTENSION_TO_CONTENT_TYPE](../reference/EXTENSION_TO_CONTENT_TYPE.md#content_types.EXTENSION_TO_CONTENT_TYPE), with 364 bare lowercase extensions as keys. [get_content_type()](../reference/get_content_type.md#content_types.get_content_type) normalises its input to the last dot-separated segment, lowercases it, and reads the dictionary. The reverse functions invert the same dictionary the first time they are called and cache the result for the life of the process. Nothing is read from disk, no system `mime.types` file is consulted, and the answers are the same on every platform and every Python version.


# Why not the standard library

Python ships a `mimetypes` module and for a while it looked like the obvious choice. Two things made it a poor fit.

First, coverage. The built-in table in `mimetypes` has 142 entries on Python 3.10 and grew to about 210 on Python 3.15, and the answers you get depend on which Python you run. Between 170 and 220 of this library's extensions are missing from it, depending on the version. Examples that are missing on every supported Python include `.tgz`, `.parquet`, `.ipynb`, `.rs`, `.go`, `.tsx`, `.psd`, and `.dwg`. Newer Pythons have added `.yaml`, `.toml`, `.webp`, `.flac`, `.epub`, and `.mkv`, so a program that worked on 3.15 can silently return `None` for those on 3.12.

Second, correctness. `mimetypes` still returns `text/xml` for `.xml`, where [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types) and current practice say `application/xml`. This library standardises on the modern type and treats the legacy spelling as an alias on reverse lookup. Other deliberate choices: `.js` is `text/javascript`, `.yaml` and `.yml` are `application/yaml` per RFC 9512, and `.md` is `text/markdown`.

The API differs too. [get_content_type()](../reference/get_content_type.md#content_types.get_content_type) returns one string, not the `(type, encoding)` tuple that `mimetypes.guess_type()` returns, and it never returns `None` unless you ask for that with `fallback=None`. The reverse functions keep the standard library names, [guess_extension()](../reference/guess_extension.md#content_types.guess_extension) and [guess_all_extensions()](../reference/guess_all_extensions.md#content_types.guess_all_extensions), but accept full header values with parameters, resolve legacy aliases, and can pick a different canonical extension, for example `.html` for `text/html`.

To see the exact differences on your interpreter, run the comparison script from the repository.

``` bash
uv run python samples/compare_to_builtin.py
```


# Why not python-magic

`python-magic` and similar libraries identify a file by reading its leading bytes. That is more reliable when you have the bytes, and it is the right tool when the extension is missing or lying. This library exists for the other case: you know the name but not the contents, such as an object key in S3 or a URL you have not fetched. The two are complementary, and `fallback=None` is the hook for falling through to byte sniffing on a miss. See [Unknown extensions](unknown-extensions.md).


# What is in the table

With 364 extensions mapped, the table covers images including camera RAW formats, audio, video, archives and modern compression formats, office and OpenDocument files, source code for around thirty languages, data science formats such as Parquet, Arrow, HDF5, pickle, NumPy, R, Stata, SAS, and SPSS, configuration and infrastructure files, Adobe and CAD formats, game engine assets, scientific formats such as FITS, DICOM, and NIfTI, and subtitles. The [reference page](../reference/EXTENSION_TO_CONTENT_TYPE.md) shows every entry.
