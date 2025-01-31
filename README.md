
# content-types 🗃️🔎

A Python library to map file extensions to MIME types. 
It also provides a CLI for quick lookups right from your terminal.
If no known mapping is found, the tool returns `application/octet-stream`.

Unlike other libraries, this one does **not** try to access the file 
or parse the bytes of the file or stream. It just looks at the extension
which is valuable when you don't have access to the file directly.
For example, you know the filename but it is stored in s3 and you don't want
to download it just to fully inspect the file.

## Installation

```bash
uv pip install content-types
```

## Usage

```python
import content_types

# Forward lookup: filename -> MIME type
mime_type = content_types.get_content_type("example.jpg")
print(mime_type)  # "image/jpeg"

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

## Contributing

Contributions are welcome! Check out [the GitHub repo](https://github.com/mikeckennedy/content-types) 
for more details on how to get involved.
