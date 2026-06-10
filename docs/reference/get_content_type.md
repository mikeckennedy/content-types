## get_content_type()


Return the most specific, commonly accepted MIME type for a filename or extension.


Usage

``` python
get_content_type(
    filename_or_extension,
    treat_as_binary=True,
    fallback=None,
)
```


The lookup is based purely on the extension -- the file's bytes are never read. A filename, a bare extension (with or without a leading dot), or a `pathlib.Path` are all accepted. For URLs, any query string (`?...`) or fragment (`#...`) is stripped first; for compound extensions the last segment wins (`archive.tar.gz` resolves as `gz`). Matching is case-insensitive.


## Parameters


`filename_or_extension: str | Path`  
A filename, path, URL, or bare extension to look up. Accepts a `str` or a `pathlib.Path`.

`treat_as_binary: bool = ``True`  
Selects the default fallback when the extension is unknown and no explicit `fallback` is given. `True` (default) returns `application/octet-stream`; `False` returns `text/plain`.

`fallback: Optional[str] = None`  
An explicit MIME type to return for unknown extensions. When provided, it takes precedence over `treat_as_binary`.


## Returns


`str`  
The mapped MIME type, or the chosen fallback when the extension is unknown.


## Raises


`TypeError`  
If `filename_or_extension` is `None`.


## Example

``` python
>>> get_content_type("picture.jpg")
'image/jpeg'
>>> get_content_type(".webp")
'image/webp'
>>> get_content_type("script.js")
'text/javascript'
>>> get_content_type("unknown.xyz")
'application/octet-stream'
>>> get_content_type("unknown.xyz", treat_as_binary=False)
'text/plain'
>>> get_content_type("unknown.xyz", fallback='application/x-custom')
'application/x-custom'
```
