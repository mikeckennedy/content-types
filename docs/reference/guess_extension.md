## guess_extension()


Return the canonical file extension for a MIME / content type.


Usage

``` python
guess_extension(
    content_type,
    with_dot=True,
)
```


This is the reverse of get_content_type(). The lookup is case-insensitive and any MIME parameters are ignored, so an HTTP `Content-Type` header value such as `text/html; charset=utf-8` resolves the same as `text/html`. Common non-canonical or legacy spellings are also accepted -- `text/json` resolves like `application/json` and `image/jpg` like `image/jpeg`. When a content type maps to several extensions, the canonical one is returned (e.g. `image/jpeg` -\> `.jpg`); use guess_all_extensions() to get every extension.

The canonical choice follows this library's table and may differ from the standard library `mimetypes` module -- for example, this returns `.html` for `text/html`.


## Parameters


`content_type: str`  
A MIME type to look up, optionally with parameters (e.g. `application/pdf` or `text/html; charset=utf-8`).

`with_dot: bool = ``True`  
When `True` (default) the returned extension has a leading dot (e.g. `.pdf`), which is what you concatenate onto a filename. When `False` the bare extension is returned (e.g. [pdf](pdf.md#content_types.pdf)).


## Returns


`Optional[str]`  
The canonical extension for the content type, or `None` if it is unknown

(including empty, whitespace-only, or parameter-only input).


## Raises


`TypeError`  
If `content_type` is `None`.


## Example

``` python
>>> guess_extension("application/pdf")
'.pdf'
>>> guess_extension("image/jpeg")
'.jpg'
>>> guess_extension("text/html; charset=utf-8")
'.html'
>>> guess_extension("application/pdf", with_dot=False)
'pdf'
>>> guess_extension("application/x-does-not-exist") is None
True
```
