# FAQ

Short answers to the questions that come up most, with links to the pages that go deeper.


# Does it read the file?

No. Every function works from the name alone. The file does not need to exist and no bytes are read. If you need byte-level detection, use a sniffing library and fall back to it on a miss as shown in [Unknown extensions](unknown-extensions.md).


# Why did I get `application/octet-stream`?

Either the extension is not in the table, or it is one of the formats that genuinely map to that type, such as `.bin`, `.pkl`, or `.npy`. Pass `fallback=None` to distinguish the two: a real `application/octet-stream` entry still returns the string, while a miss returns `None`.


# Is `.tar.gz` handled as a unit?

No. The last segment wins, so `archive.tar.gz` returns `application/gzip`, which is the correct type for the compressed container. There is no special casing for double extensions.


# Does it handle uppercase or mixed case?

Yes. Extensions are lowercased before the lookup, and content types are lowercased in the reverse direction.


# Does it handle URLs?

Yes. Query strings and fragments are stripped before the lookup, so `https://cdn.example.com/a.mp3?v=3` returns `audio/mpeg`. A URL with no file component, such as `https://example.com/download`, is a miss.


# Why do my `Path` and string results disagree for dotfiles?

They should not. Both `Path('.env')` and the string `'.env'` return `text/plain`. Versions before the next release used `Path.suffix`, which is empty for a dotfile, so the `Path` form fell through to the fallback. That is fixed.


# The type checker says [get_content_type()](../reference/get_content_type.md#content_types.get_content_type) returns `Optional[str]`

It returns `str` unless you pass `fallback=None`. The function is overloaded so that the default call and a string `fallback` type as `str`, and only an explicit `fallback=None` types as `Optional[str]`. If your checker still shows the wider type, you are on a release before the next one.


# Can I add or override an extension?

Yes. Assign into [content_types.EXTENSION_TO_CONTENT_TYPE](../reference/EXTENSION_TO_CONTENT_TYPE.md#content_types.EXTENSION_TO_CONTENT_TYPE) with a bare lowercase key. Do it at startup and before the first reverse lookup, because the reverse map is built once and cached. For formats other people would expect, open an issue so the table is fixed for everyone.


# Why does `guess_extension('text/html')` return `.html` and not `.htm`?

Because `.html` is what people write today. The library keeps a short list of canonical overrides where the first-listed extension in the table is the less common spelling. The standard library makes different choices, so do not expect the two to agree on canonical extensions.


# What about `text/yaml` or `application/x-yaml`?

The forward direction returns `application/yaml` for `.yaml` and `.yml`, following RFC 9512. The reverse direction accepts the legacy spellings as aliases and returns `.yaml`.


# Is it thread-safe?

Yes for reads. The forward lookup is a dictionary read and the reverse map is built with `functools.cache`. If you mutate the table at import time or startup, do it before spawning threads.


# How do I run the tests?

``` bash
uv run --with pytest pytest
```

See the [README](https://github.com/mikeckennedy/content-types#development) for lint and docs commands.
