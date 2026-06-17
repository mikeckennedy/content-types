## guess_all_extensions()


Return every known file extension for a MIME / content type, canonical first.


Usage

``` python
guess_all_extensions(
    content_type,
    with_dot=True,
)
```


Like guess_extension(), but returns the full list rather than just the canonical extension. The lookup is case-insensitive, MIME parameters are ignored, and common non-canonical spellings (e.g. `text/json`, `image/jpg`) resolve to their canonical type. The first element always equals guess_extension(content_type). The order follows this library's table (canonical first) and is not guaranteed to match the standard library `mimetypes` module.


## Parameters


`content_type: str`  
A MIME type to look up, optionally with parameters (e.g. `image/jpeg` or `text/html; charset=utf-8`).

`with_dot: bool = ``True`  
When `True` (default) each extension has a leading dot (e.g. `.jpg`); when `False` the bare extensions are returned (e.g. [jpg](jpg.md#content_types.jpg)).


## Returns


`list[str]`  
A list of extensions, canonical first, or an empty list if the content type is

unknown (including empty, whitespace-only, or parameter-only input).


## Raises


`TypeError`  
If `content_type` is `None`.


## Example

``` python
>>> guess_all_extensions("image/jpeg")
['.jpg', '.jpeg', '.jpe']
>>> guess_all_extensions("text/html")
['.html', '.htm']
>>> guess_all_extensions("application/pdf")
['.pdf']
>>> guess_all_extensions("application/x-does-not-exist")
[]
```
