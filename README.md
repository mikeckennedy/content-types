
# content-types 🗃️🔎

A Python library to map file extensions to MIME types. 
It also provides a CLI for quick lookups right from your terminal.
If no known mapping is found, the tool returns `application/octet-stream`.

Unlike other libraries, this one does **not** try to access the file 
or parse the bytes of the file or stream. It just looks at the extension
which is valuable when you don't have access to the file directly.
For example, you know the filename but it is stored in s3 and you don't want
to download it just to fully inspect the file.

Why not just use Python's built-in `mimetypes`? Or the excellent `python-magic` package? See below.

## Installation

```bash
uv pip install content-types
```

## Usage

```python
import content_types

# Forward lookup: filename -> MIME type
the_type = content_types.get_content_type("example.jpg")
print(the_type)  # "image/jpeg"

# For very common files, you have shortcuts:
print(f'Content-Type for webp is {content_types.webp}.') 
# Content-Type for webp is image/webp.
```

## CLI

To use the library as a CLI tool, just install it with **uv** or **pipx**. 

```bash
uv tool install content-types
```

Now it will be available machine-wide.

```bash
content-types example.jpg

# Outputs image/jpeg
```

## More correct than Python's `mimetypes`

When I first learned about Python's mimetypes module, I thought it was exactly what I need. However, 
it doesn't have all the MIME types. And, it recommends deprecated, out-of-date answers for very obvious types.

For example, mimetypes has `.xml` as text/xml  where it should be `application/xml` 
(see [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/MIME_types/Common_types)).

And mimetypes is missing important types such as:

- .m4v  -> video/mp4
- .tgz  -> application/gzip
- .flac -> audio/flac
- .epub -> application/epub+zip
- ...

Here is a full comparison found by running `samples/compare_to_builtin.py`:

```text
There are 5 types where mimetypes and content-types disagree

mimetypes: .wav audio/x-wav, content-types: .wav audio/wav
mimetypes: .obj application/octet-stream, content-types: .obj model/obj
mimetypes: .xml text/xml, content-types: .xml application/xml
mimetypes: .exe application/octet-stream, content-types: .exe application/x-msdownload
mimetypes: .dll application/octet-stream, content-types: .dll application/x-msdownload

There are 0 types in mimetypes that are not in content-types

There are 31 types in content-types that are not in mimetypes

.docx -> application/vnd.openxmlformats-officedocument.wordprocessingml.document
.m4v  -> video/mp4
.odp  -> application/vnd.oasis.opendocument.presentation
.deb  -> application/x-debian-package
.glb  -> model/gltf-binary
.php  -> application/x-httpd-php
.xlsx -> application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
.woff -> font/woff
.tgz  -> application/gzip
.ogg  -> audio/ogg
.odt  -> application/vnd.oasis.opendocument.text
.wmv  -> video/x-ms-wmv
.stl  -> model/stl
.ttf  -> font/ttf
.flac -> audio/flac
.rar  -> application/vnd.rar
.odg  -> application/vnd.oasis.opendocument.graphics
.ods  -> application/vnd.oasis.opendocument.spreadsheet
.weba -> audio/webm
.gltf -> model/gltf+json
.epub -> application/epub+zip
.m4a  -> audio/mp4
.map  -> application/json
.pptx -> application/vnd.openxmlformats-officedocument.presentationml.presentation
.woff2 -> font/woff2
.otf  -> font/otf
.gz   -> application/gzip
.rpm  -> application/x-rpm
.7z   -> application/x-7z-compressed
.ogv  -> video/ogg
.apk  -> application/vnd.android.package-archive
```


## Contributing

Contributions are welcome! Check out [the GitHub repo](https://github.com/mikeckennedy/content-types) 
for more details on how to get involved.
