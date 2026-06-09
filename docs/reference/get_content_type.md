## get_content_type()


Given a filename (or just an extension), return the most specific,


Usage

``` python
get_content_type(
    filename_or_extension,
    treat_as_binary=True,
    fallback=None,
)
```


commonly accepted MIME type based on extension.

Falls back to 'application/octet-stream' if `treat_as_binary` is True (default) and 'text/plain' if it is False when the extension is not known.

To override the fallback, pass `fallback='application/x-custom'` (or any string you'd like returned for unknown extensions). When `fallback` is provided, it takes precedence over `treat_as_binary`.


## Example

> > > get_content_type("picture.jpg") 'image/jpeg' get_content_type(".webp") 'image/webp' get_content_type("script.js") 'text/javascript' get_content_type("unknown.xyz") 'application/octet-stream' get_content_type("unknown.xyz", treat_as_binary=False) 'text/plain' get_content_type("unknown.xyz", fallback='application/x-custom') 'application/x-custom'
