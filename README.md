
# content-types 🗃️🔎

A comprehensive Python library to map file extensions to MIME types with **360+ supported formats**. 
It also provides a CLI for quick lookups right from your terminal.
If no known mapping is found, the tool returns `application/octet-stream`.

Unlike other libraries, this one does **not** try to access the file 
or parse the bytes of the file or stream. It just looks at the extension
which is valuable when you don't have access to the file directly.
For example, you know the filename but it is stored in s3 and you don't want
to download it just to fully inspect the file.

## Extensive Format Support

With **360+ file extensions** mapped, content-types covers:

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

...and much more!

Why not just use Python's built-in `mimetypes`? Or the excellent `python-magic` package? 
[See below](#more-correct-than-pythons-mimetypes).

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

# Works with any supported extension
print(content_types.get_content_type("data.parquet"))  # "application/vnd.apache.parquet"
print(content_types.get_content_type("notebook.ipynb"))  # "application/x-ipynb+json"
print(content_types.get_content_type("photo.cr2"))  # "image/x-canon-cr2"
print(content_types.get_content_type("model.blend"))  # "application/x-blender"
print(content_types.get_content_type("contract.sol"))  # "text/x-solidity"

# For very common files, you have shortcuts:
print(f'Content-Type for webp is {content_types.webp}.') 
# Content-Type for webp is image/webp.

# Data science shortcuts
print(content_types.parquet)  # "application/vnd.apache.parquet"
print(content_types.ipynb)    # "application/x-ipynb+json"
print(content_types.yaml)     # "text/yaml"
print(content_types.toml)     # "application/toml"

# Works with Path objects too
from pathlib import Path
path = Path("document.pdf")
print(content_types.get_content_type(path))  # "application/pdf"
```

## CLI

To use the library as a CLI tool, just install it with **uv** or **pipx**. 

```bash
uv tool install content-types
```

Now it will be available machine-wide.

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
- .parquet -> application/vnd.apache.parquet
- .ipynb -> application/x-ipynb+json
- .mkv -> video/x-matroska
- .toml -> application/toml
- .yaml -> text/yaml
- .rs -> text/x-rust
- .go -> text/x-go
- .tsx -> text/tsx
- .psd -> image/vnd.adobe.photoshop
- .dwg -> application/acad
- ... and 300+ more

With this library, you get **360+ file extensions** properly mapped, compared to Python's `mimetypes` 
which only has around 100 and includes outdated MIME types.

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

## Works when python-magic package doesn't

Why not the excellent python-magic package? That one works by reading the header bytes of
binary files which requires access to the file data. The whole goal of this project is
to avoid accessing or needing the file data. They are for different use-cases.

## Contributing

Contributions are welcome! Check out [the GitHub repo](https://github.com/mikeckennedy/content-types) 
for more details on how to get involved.
