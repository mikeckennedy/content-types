# Unknown extensions

Every lookup returns something. That is convenient right up to the moment you need to know whether the answer was a confident match or a shrug. This page is about telling the two apart, and about what to do once you can.


# The shrug looks like an answer

[get_content_type()](../reference/get_content_type.md#content_types.get_content_type) returns a string unless you ask it not to. For a known extension the string is the content type. For an unknown one it is a fallback, and the default fallback is `application/octet-stream`.

``` python
import content_types

content_types.get_content_type('data.parquet')  # 'application/vnd.apache.parquet'
content_types.get_content_type('notes.xyz')  # 'application/octet-stream'
content_types.get_content_type('Makefile')  # 'application/octet-stream'
```

`application/octet-stream` is a perfectly good header. It is what S3 and most web servers send when they do not know better, and browsers respond by offering a download, which is the safe move for mystery bytes. The trouble is that it is also a real answer. A handful of formats genuinely map to it, on purpose, because there is no better registered type: `.bin`, `.pkl`, `.npy`, `.so`, `.o`, and a few more. So when you see `application/octet-stream` come back, you cannot tell from the string alone whether the table recognised the extension or gave up.

Think of it as a detective who, when stumped, writes "unknown substance" on the report. Useful, as long as you remember that some substances really are labelled "unknown substance".


# Three ways to handle a miss

**Change the shrug.** If the files you deal with are mostly text, tell the lookup to shrug in the other direction. `treat_as_binary=False` swaps the default fallback for `text/plain`.

``` python
content_types.get_content_type('notes.xyz', treat_as_binary=False)  # 'text/plain'
```

**Write your own shrug.** Pass any string as `fallback` and that is what comes back for every unknown extension. It outranks `treat_as_binary`. Known extensions are untouched.

``` python
content_types.get_content_type('notes.xyz', fallback='application/x-acme')  # 'application/x-acme'
content_types.get_content_type('photo.jpg', fallback='application/x-acme')  # 'image/jpeg'
```

**Refuse to shrug.** Pass `fallback=None` and a miss comes back as `None`. Now you can branch. This is the mode to use when a miss should change what the program does next, for example to hand the file to a byte-sniffing library, to reject the upload, or to log it for a human.

``` python
content_type = content_types.get_content_type(name, fallback=None)
if content_type is None:
    content_type = sniff_with_python_magic(path)
```

One subtlety that bites people who skim: leaving `fallback` out and passing `fallback=None` are different things. Leaving it out keeps the historical default. The parameter's real default is a private sentinel, precisely so that an explicit `None` can mean "give me `None`" without changing behaviour for every caller who never passes the argument. Your type checker knows this too. The plain call types as `str`, and only `fallback=None` widens it to `Optional[str]`.


# Ask the table directly

If you only want a yes or a no, skip the function and ask the table. Keys are bare lowercase extensions with no leading dot.

``` python
ext = 'parquet'
ext in content_types.EXTENSION_TO_CONTENT_TYPE  # True
```


# Teaching it a new word

The table is a plain `dict`, and the forward lookup reads it fresh on every call, so an addition takes effect immediately. Keys must be lowercase and have no leading dot.

``` python
content_types.EXTENSION_TO_CONTENT_TYPE['acme'] = 'application/x-acme'
content_types.get_content_type('report.acme')  # 'application/x-acme'
```

Do this once at startup, not inside a request handler. And do it before the first reverse lookup, because [guess_extension()](../reference/guess_extension.md#content_types.guess_extension) builds its inverted view of the table on first use and caches it for the life of the process. Additions made after that are visible to the forward lookup but invisible to the reverse one.

If the extension is a real, widely used format that other people would reasonably expect to work, do not keep the fix to yourself. [Open an issue](https://github.com/mikeckennedy/content-types/issues) or send a pull request and it ends up in the table for everyone.


# Things that look like misses but are not

- `None` as the filename raises `TypeError`. That is a bug in the caller, not an unknown extension, and the library refuses to paper over it.
- `archive.tar.gz` returns `application/gzip`. That is a hit on the last segment, and it is the correct type for the compressed container.

And things that are misses, in case you were wondering: an empty string, a name with no dot anywhere, and a URL with no file component such as `https://example.com/download`. All three get the fallback.
