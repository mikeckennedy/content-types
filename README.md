# content-types 🗃️🔎

[![PyPI version](https://img.shields.io/pypi/v/content-types.svg)](https://pypi.org/project/content-types/)
[![Python versions](https://img.shields.io/pypi/pyversions/content-types.svg)](https://pypi.org/project/content-types/)
[![License: MIT](https://img.shields.io/pypi/l/content-types.svg)](https://github.com/mikeckennedy/content-types/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-mkennedy.codes-2188ff.svg)](https://mkennedy.codes/docs/content-types/)

Someone hands you a sealed envelope and asks what is inside. You are not allowed to open it. All you get is the label on the front.

That is the situation every time you need a `Content-Type` for a file you cannot, or would rather not, read. The object is in S3 and fetching it just to peek at the header bytes is slow and costs money. The URL has not been downloaded yet. The upload has a name but the bytes are still streaming in. In every one of those cases the label is right there, and the label is usually enough.

content-types reads the label. Give it a filename, a path, a bare extension, a `pathlib.Path`, or a URL, and it returns the MIME type from a table of **360+ extensions**. It never opens, reads, or sniffs the file. It also runs the other way, turning a content type or a raw `Content-Type` header back into a file extension, and it ships a tiny command line tool for the moments when the question is in your terminal rather than your code.

```python
import content_types

content_types.get_content_type('invoice-2026-03.pdf')  # 'application/pdf'
content_types.get_content_type('s3://bucket/photos/IMG_4021.CR2')  # 'image/x-canon-cr2'
content_types.guess_extension('text/html; charset=utf-8')  # '.html'
```

Zero dependencies, pure Python, Python 3.10 and up.

## 📚 Documentation

Full documentation is hosted at **[mkennedy.codes/docs/content-types](https://mkennedy.codes/docs/content-types/)**. The quick tour below covers the essentials; the docs go deeper:

- [Getting started](https://mkennedy.codes/docs/content-types/user-guide/getting-started.html): install, first lookup, and every input shape the lookup accepts.
- [Unknown extensions](https://mkennedy.codes/docs/content-types/user-guide/unknown-extensions.html): how to tell a miss from a real `application/octet-stream`, and the three ways to handle one.
- [Reverse lookup](https://mkennedy.codes/docs/content-types/user-guide/reverse-lookup.html): from a content type or `Content-Type` header back to an extension, and why that direction is the hard one.
- [Command line](https://mkennedy.codes/docs/content-types/user-guide/cli.html): the `content-types` script, its flags, and exit codes.
- [Compared to mimetypes](https://mkennedy.codes/docs/content-types/user-guide/compared-to-mimetypes.html): why the standard library was not enough and how the table differs.
- [FAQ](https://mkennedy.codes/docs/content-types/user-guide/faq.html) and the searchable [API reference](https://mkennedy.codes/docs/content-types/reference/).

Coding agents can read [llms-full.txt](https://mkennedy.codes/docs/content-types/llms-full.txt) or install the [skill](https://mkennedy.codes/docs/content-types/skills.html).

## What is in the table

The 360+ extensions cover far more than the usual web suspects:

- 🎨 **Images** - Standard formats plus RAW camera files (Canon, Nikon, Sony, Adobe DNG, etc.)
- 🎵 **Audio** - MP3, FLAC, AAC, MIDI, WMA, ALAC, DSD, and more
- 🎬 **Video** - MP4, MKV, WebM, FLV, and modern codecs
- 📦 **Archives** - ZIP, TAR, 7Z, RAR, plus modern formats (bz2, xz, zstd, brotli)
- 📄 **Documents** - PDF, Office formats (DOCX, XLSX, PPTX), OpenDocument
- 💻 **Programming** - Python, JavaScript, TypeScript, Rust, Go, Java, C++, Swift, Kotlin, and 25+ languages
- 🔬 **Data Science** - Parquet, Jupyter notebooks, HDF5, Arrow, Pickle, NumPy, R, Stata, SAS, SPSS
- ⚙️ **Configuration** - YAML, TOML, JSON, INI, ENV, dotfiles
- 🐳 **DevOps** - Dockerfiles, Terraform, Kubernetes configs, Nomad
- 🎨 **Creative Suite** - Adobe (PSD, InDesign, Premiere, After Effects), CAD files (AutoCAD, SketchUp, Blender)
- 🎮 **Game Development** - Unity, Unreal Engine, PAK files
- 🔬 **Scientific** - FITS, DICOM, NIfTI, PDB (protein data)
- ⛓️ **Blockchain** - Solidity, Vyper smart contracts
- 🗄️ **Databases** - SQLite, Access, MySQL files
- 📝 **Documentation** - Markdown, AsciiDoc, Org-mode, BibTeX

...and much more. The [reference page](https://mkennedy.codes/docs/content-types/reference/EXTENSION_TO_CONTENT_TYPE.html) lists every entry.

Why not just use Python's built-in `mimetypes`? Or the excellent `python-magic` package? [See below](#more-correct-than-pythons-mimetypes).

## Installation

Requires Python 3.10 or later. There are no runtime dependencies, so it adds nothing to your lock file but itself.

```bash
uv add content-types
# or
pip install content-types
```

## Usage

The forward lookup is one function. It is not fussy about what you hand it.

```python
import content_types

# Forward lookup: filename -> MIME type
the_type = content_types.get_content_type('example.jpg')
print(the_type)  # 'image/jpeg'

# Works with any supported extension
print(content_types.get_content_type('data.parquet'))  # 'application/vnd.apache.parquet'
print(content_types.get_content_type('notebook.ipynb'))  # 'application/x-ipynb+json'
print(content_types.get_content_type('photo.cr2'))  # 'image/x-canon-cr2'
print(content_types.get_content_type('model.blend'))  # 'application/x-blender'
print(content_types.get_content_type('contract.sol'))  # 'text/x-solidity'

# Case does not matter, and a bare extension works with or without the dot
print(content_types.get_content_type('PHOTO.JPG'))  # 'image/jpeg'
print(content_types.get_content_type('.webp'))  # 'image/webp'
print(content_types.get_content_type('webp'))  # 'image/webp'

# Path objects work
from pathlib import Path

path = Path('document.pdf')
print(content_types.get_content_type(path))  # 'application/pdf'

# URLs work: query strings and fragments are stripped before the lookup
url = 'https://cdn.example.com/song.mp3?cache_id=678c2a'
print(content_types.get_content_type(url))  # 'audio/mpeg'

# For very common files there are shortcuts, plain strings ready for a header
print(f'Content-Type for webp is {content_types.webp}.')
# Content-Type for webp is image/webp.
print(content_types.parquet)  # 'application/vnd.apache.parquet'
print(content_types.ipynb)  # 'application/x-ipynb+json'
print(content_types.yaml)  # 'application/yaml'
print(content_types.toml)  # 'application/toml'
print(content_types.sqlite)  # 'application/vnd.sqlite3'
```

### When the label is blank

An unknown extension does not raise. By default it returns `application/octet-stream`, the universal "it is bytes" type, which is the right thing to put in a header but hides the fact that the lookup missed. You get to choose how loud a miss should be.

```python
# The default shrug
print(content_types.get_content_type('notes.unknownext'))  # 'application/octet-stream'

# Shrug towards text instead
print(content_types.get_content_type('notes.unknownext', treat_as_binary=False))  # 'text/plain'

# Your own placeholder; it outranks treat_as_binary and known extensions are unaffected
print(content_types.get_content_type('notes.unknownext', fallback='application/x-custom'))  # 'application/x-custom'

# Refuse to shrug: get None back and branch on it
print(content_types.get_content_type('notes.unknownext', fallback=None))  # None
print(content_types.get_content_type('photo.jpg', fallback=None))  # 'image/jpeg' (known, unaffected)
```

Omitting `fallback` and passing `fallback=None` are different on purpose, so existing callers never see a `None` they did not ask for. Your type checker agrees: the plain call is `str`, and only `fallback=None` widens it to `Optional[str]`. The full story, including how to tell a real `.pkl` from a miss, is in [Unknown extensions](https://mkennedy.codes/docs/content-types/user-guide/unknown-extensions.html).

### Running the envelope backwards

A server has just told you what is inside, as a `Content-Type` header, and you need to write a label. That is the reverse lookup, and it reads headers the way servers actually send them: any case, with parameters, and with the legacy spellings that never quite went away.

```python
# Reverse lookup: MIME type -> extension (the inverse of get_content_type)
print(content_types.guess_extension('application/pdf'))  # '.pdf'
print(content_types.guess_extension('image/jpeg'))  # '.jpg' (the canonical pick)
print(content_types.guess_all_extensions('image/jpeg'))  # ['.jpg', '.jpeg', '.jpe']

# Case-insensitive, and parameters on a Content-Type header are ignored
print(content_types.guess_extension('text/html; charset=utf-8'))  # '.html'

# Legacy and mistaken spellings resolve to the canonical type
print(content_types.guess_extension('text/json'))  # '.json'  (canonical: application/json)
print(content_types.guess_extension('image/jpg'))  # '.jpg'   (canonical: image/jpeg)

# Pass with_dot=False for a bare extension; unknown types return None / []
print(content_types.guess_extension('application/toml', with_dot=False))  # 'toml'
print(content_types.guess_extension('application/x-nope'))  # None
print(content_types.guess_all_extensions('application/x-nope'))  # []
```

The reverse direction is the hard one. The table's 364 extensions collapse onto 223 types, and 57 of those types have more than one extension claiming them, so somebody has to pick a canonical spelling and keep it stable. This library picks the modern one (`.html` for `text/html`, not `.htm`) and guarantees that `guess_extension(t)` always equals `guess_all_extensions(t)[0]`. See [Reverse lookup](https://mkennedy.codes/docs/content-types/user-guide/reverse-lookup.html) for the details.

## CLI

Sometimes the question is in your terminal. Install the tool with **uv** or **pipx** and it is available machine-wide.

```bash
uv tool install content-types
```

```bash
content-types example.jpg
# Outputs: image/jpeg

content-types data.parquet
# Outputs: application/vnd.apache.parquet

content-types notebook.ipynb
# Outputs: application/x-ipynb+json

content-types photo.cr2
# Outputs: image/x-canon-cr2
```

It does the forward lookup only. An unknown extension prints `application/octet-stream` and exits 0; no argument prints the usage text and exits 1; `-h`, `--help`, and `--version` do what you expect. See [Command line](https://mkennedy.codes/docs/content-types/user-guide/cli.html).

## More correct than Python's `mimetypes`

When I first learned about Python's mimetypes module, I thought it was exactly what I needed. Then I used it. It does not have all the MIME types, and for some very obvious ones it recommends answers that stopped being right years ago.

For example, mimetypes has `.xml` as `text/xml` where it should be `application/xml` (see [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types)).

Its coverage also depends on which Python you happen to be running. The built-in table has 142 entries on Python 3.10 and about 210 on Python 3.15, so an extension that resolves on your laptop can come back `None` on an older production image. Types missing from mimetypes on every supported Python include:

- .tgz -> application/gzip
- .parquet -> application/vnd.apache.parquet
- .ipynb -> application/x-ipynb+json
- .rs -> text/x-rust
- .go -> text/x-go
- .tsx -> text/tsx
- .psd -> image/vnd.adobe.photoshop
- .dwg -> application/acad
- ... and 170 to 220 more, depending on your Python version

Older Pythons are also missing everyday types such as `.webp`, `.yaml`, `.toml`, `.flac`, `.epub`, and `.mkv` that newer releases have since added. With this library, you get **360+ file extensions** properly mapped, with the same answers on every Python version and every operating system. See [Compared to mimetypes](https://mkennedy.codes/docs/content-types/user-guide/compared-to-mimetypes.html) for how the lookup works and a script that prints the exact differences on your interpreter.

## Works when python-magic package doesn't

Why not the excellent python-magic package? That one works by reading the header bytes of a file, which is the more reliable method when you have the bytes and the only method when the extension is missing or lying. The whole point of this project is the other case: you know the name but not the contents. The two are not rivals, and `fallback=None` is the hook for handing a miss over to byte sniffing when you do have the file.

## Popular Format Examples

Here are some commonly used formats by category:

**Data Science & Analytics:**

- `.parquet` - Apache Parquet columnar storage
- `.ipynb` - Jupyter Notebooks
- `.pkl`, `.pickle` - Python pickle files
- `.npy`, `.npz` - NumPy arrays
- `.arrow`, `.feather` - Apache Arrow
- `.hdf5`, `.h5` - HDF5 scientific data
- `.mat` - MATLAB data files
- `.dta` - Stata data files
- `.sav` - SPSS data files

**Modern Programming Languages:**

- `.rs` - Rust
- `.go` - Go/Golang
- `.ts`, `.tsx` - TypeScript/React
- `.jsx` - React JavaScript
- `.vue` - Vue.js components
- `.swift` - Swift
- `.kt`, `.kts` - Kotlin
- `.dart` - Dart
- `.sol` - Solidity (smart contracts)

**Configuration & Infrastructure:**

- `.yaml`, `.yml` - YAML configs
- `.toml` - TOML configs
- `.env` - Environment variables
- `.dockerfile` - Docker files
- `.tf`, `.tfvars` - Terraform
- `.ini`, `.conf`, `.cfg` - Configuration files

**Creative & Design:**

- `.psd`, `.psb` - Adobe Photoshop
- `.indd` - Adobe InDesign
- `.aep` - Adobe After Effects
- `.dwg`, `.dxf` - AutoCAD
- `.skp` - SketchUp
- `.blend` - Blender
- `.cr2`, `.cr3` - Canon RAW
- `.nef` - Nikon RAW
- `.dng` - Adobe DNG RAW

**Modern Media:**

- `.mkv` - Matroska video
- `.webp` - WebP images
- `.avif` - AVIF images
- `.opus` - Opus audio
- `.flac` - FLAC audio
- `.midi`, `.mid` - MIDI

## Contributing

Contributions are welcome, and the most useful one is also the easiest: if an extension you rely on is missing or wrong, [open an issue](https://github.com/mikeckennedy/content-types/issues) with the extension and the type you expected. Check out [the GitHub repo](https://github.com/mikeckennedy/content-types) for more details on how to get involved.

### Development

`pytest` and `ruff` aren't declared dependencies; `uv` provides them on the fly:

```bash
# Run the test suite (75 tests)
uv run --with pytest pytest

# Lint and format (config in ruff.toml)
uvx ruff check .
uvx ruff format .
```

### Building the docs

The docs site is built with [Great Docs](https://github.com/posit-dev/great-docs) and published at [mkennedy.codes/docs/content-types](https://mkennedy.codes/docs/content-types/). The user guide lives in `user_guide/`, the agent skill in `skills/content-types/SKILL.md`, and the landing page is this README. Great Docs imports the package for API introspection, so the toolchain lives in the `dev` extra and needs an editable install:

```bash
# Install the docs toolchain into your virtualenv
uv pip install -e ".[dev]"

# Build the site (mirrors great-docs/_site/ into the committed docs/ folder;
# fails if llms.txt, llms-full.txt, or skill.md did not get generated)
python scripts/build_docs.py

# Preview exactly as hosted, under the /docs/content-types subpath
python scripts/serve_docs.py   # -> http://127.0.0.1:8099/docs/content-types/
```
