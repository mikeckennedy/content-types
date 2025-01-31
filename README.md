
# content-types 🗃️🔎

A Python library to map file extensions to MIME types (and vice versa). 
It also provides a CLI for quick lookups right from your terminal.
If no known mapping is found, the tool returns `application/octet-stream`.

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

# Reverse lookup: MIME type -> extensions
extensions = content_types.get_extensions_for_content_type("image/jpeg")
print(extensions) # [".jpg", ".jpeg"]

# For very common files, you have shortcuts:
print(f'Content-Type for webp is {content_types.webp}')
```

## CLI

After installing in a virtual environment or system-wide.

```bash
contenttypes example.jpg

# Outputs image/jpeg
```

## Contributing

Contributions are welcome! Check out [the GitHub repo](https://github.com/mikeckennedy/content-types) 
for more details on how to get involved.
