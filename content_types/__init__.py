import functools
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Optional

__version__ = version('content-types')

# This dictionary maps file extensions (no dot) to the most specific content type.

# noinspection SpellCheckingInspection
EXTENSION_TO_CONTENT_TYPE: dict[str, str] = {
    # Text
    'txt': 'text/plain',
    'htm': 'text/html',
    'html': 'text/html',
    'css': 'text/css',
    'csv': 'text/csv',
    'tsv': 'text/tab-separated-values',
    # JavaScript
    'js': 'text/javascript',
    # MJS for ES modules
    'mjs': 'text/javascript',
    # JSON
    'json': 'application/json',
    'map': 'application/json',
    # XML (keep application/xml)
    'xml': 'application/xml',
    # Images
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'webp': 'image/webp',
    'avif': 'image/avif',
    # Some new ones:
    'ico': 'image/vnd.microsoft.icon',
    'svg': 'image/svg+xml',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    'heic': 'image/heic',  # new
    'heif': 'image/heif',  # new
    'jpe': 'image/jpeg',  # new alias
    'ief': 'image/ief',  # new
    'ras': 'image/x-cmu-raster',  # new
    'pnm': 'image/x-portable-anymap',
    'pbm': 'image/x-portable-bitmap',
    'pgm': 'image/x-portable-graymap',
    'ppm': 'image/x-portable-pixmap',
    'rgb': 'image/x-rgb',
    'xbm': 'image/x-xbitmap',
    'xpm': 'image/x-xpixmap',
    'xwd': 'image/x-xwindowdump',
    # RAW Image Formats (Photography)
    'cr2': 'image/x-canon-cr2',
    'cr3': 'image/x-canon-cr3',
    'nef': 'image/x-nikon-nef',
    'nrw': 'image/x-nikon-nrw',
    'arw': 'image/x-sony-arw',
    'srf': 'image/x-sony-srf',
    'sr2': 'image/x-sony-sr2',
    'dng': 'image/x-adobe-dng',
    'orf': 'image/x-olympus-orf',
    'rw2': 'image/x-panasonic-rw2',
    'pef': 'image/x-pentax-pef',
    'raf': 'image/x-fuji-raf',
    'raw': 'image/x-raw',
    # Audio
    'mp3': 'audio/mpeg',
    'ogg': 'audio/ogg',
    'wav': 'audio/wav',
    'aac': 'audio/aac',
    'flac': 'audio/flac',
    'm4a': 'audio/mp4',
    'weba': 'audio/webm',
    'adts': 'audio/aac',
    'loas': 'audio/aac',
    # New ones:
    'mp2': 'audio/mpeg',  # new
    'opus': 'audio/opus',  # new
    'aif': 'audio/x-aiff',
    'aifc': 'audio/x-aiff',
    'aiff': 'audio/x-aiff',
    'au': 'audio/basic',
    'snd': 'audio/basic',
    'ra': 'audio/x-pn-realaudio',
    # Modern Audio Formats
    'midi': 'audio/midi',
    'mid': 'audio/midi',
    'ape': 'audio/x-ape',
    'wma': 'audio/x-ms-wma',
    'alac': 'audio/x-alac',
    'dsd': 'audio/dsd',
    'dsf': 'audio/x-dsf',
    # Video
    'mp4': 'video/mp4',
    'm4v': 'video/mp4',
    'mov': 'video/quicktime',
    'avi': 'video/x-msvideo',
    'wmv': 'video/x-ms-wmv',
    'mpg': 'video/mpeg',
    'mpeg': 'video/mpeg',
    'ogv': 'video/ogg',
    'webm': 'video/webm',
    # New aliases:
    'm1v': 'video/mpeg',
    'mpa': 'video/mpeg',
    'mpe': 'video/mpeg',
    'qt': 'video/quicktime',
    'movie': 'video/x-sgi-movie',
    # Modern Video Formats
    'mkv': 'video/x-matroska',
    'flv': 'video/x-flv',
    'm2ts': 'video/mp2t',
    'mts': 'video/mp2t',
    'vob': 'video/mpeg',
    'f4v': 'video/x-f4v',
    # 3GP family (prefer official video/*):
    '3gp': 'audio/3gpp',
    '3gpp': 'audio/3gpp',
    '3g2': 'audio/3gpp2',
    '3gpp2': 'audio/3gpp2',
    # Archives / Packages
    'pdf': 'application/pdf',
    'zip': 'application/zip',
    'gz': 'application/gzip',
    'tgz': 'application/gzip',
    'tar': 'application/x-tar',
    '7z': 'application/x-7z-compressed',
    'rar': 'application/vnd.rar',
    # Modern Compression Formats
    'bz2': 'application/x-bzip2',
    'tbz': 'application/x-bzip2',
    'tbz2': 'application/x-bzip2',
    'xz': 'application/x-xz',
    'txz': 'application/x-xz',
    'lz': 'application/x-lzip',
    'lzma': 'application/x-lzma',
    'zst': 'application/zstd',
    'zstd': 'application/zstd',
    'br': 'application/x-br',
    # Disk Images
    'iso': 'application/x-iso9660-image',
    'dmg': 'application/x-apple-diskimage',
    'img': 'application/x-raw-disk-image',
    'cab': 'application/vnd.ms-cab-compressed',
    'msi': 'application/x-msi',
    # Additional
    'bin': 'application/octet-stream',  # new explicit
    'a': 'application/octet-stream',
    'so': 'application/octet-stream',
    'o': 'application/octet-stream',
    'obj': 'model/obj',  # keep from original (not octet-stream)
    'dll': 'application/x-msdownload',
    'exe': 'application/x-msdownload',
    # Some additional archiving/compression tools
    'bcpio': 'application/x-bcpio',
    'cpio': 'application/x-cpio',
    'shar': 'application/x-shar',
    'sv4cpio': 'application/x-sv4cpio',
    'sv4crc': 'application/x-sv4crc',
    'ustar': 'application/x-ustar',
    'src': 'application/x-wais-source',
    # Application / Office
    'doc': 'application/msword',
    'xls': 'application/vnd.ms-excel',
    'ppt': 'application/vnd.ms-powerpoint',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    # New ones:
    'dot': 'application/msword',
    'wiz': 'application/msword',
    'xlb': 'application/vnd.ms-excel',
    'pot': 'application/vnd.ms-powerpoint',
    'ppa': 'application/vnd.ms-powerpoint',
    'pps': 'application/vnd.ms-powerpoint',
    'pwz': 'application/vnd.ms-powerpoint',
    # Additional special apps
    'webmanifest': 'application/manifest+json',
    'nq': 'application/n-quads',
    'nt': 'application/n-triples',
    'oda': 'application/oda',
    'p7c': 'application/pkcs7-mime',
    'ps': 'application/postscript',
    'ai': 'application/postscript',
    'eps': 'application/postscript',
    'trig': 'application/trig',
    'm3u': 'application/vnd.apple.mpegurl',
    'm3u8': 'application/vnd.apple.mpegurl',
    'wasm': 'application/wasm',
    'csh': 'application/x-csh',
    'dvi': 'application/x-dvi',
    'gtar': 'application/x-gtar',
    'hdf': 'application/x-hdf',
    'h5': 'application/x-hdf5',  # not in older standard lists but sometimes used
    'latex': 'application/x-latex',
    'mif': 'application/x-mif',
    'cdf': 'application/x-netcdf',
    'nc': 'application/x-netcdf',
    'p12': 'application/x-pkcs12',
    'pfx': 'application/x-pkcs12',
    'ram': 'application/x-pn-realaudio',
    'pyc': 'application/x-python-code',
    'pyo': 'application/x-python-code',
    'swf': 'application/x-shockwave-flash',
    'tcl': 'application/x-tcl',
    'tex': 'application/x-tex',
    'texi': 'application/x-texinfo',
    'texinfo': 'application/x-texinfo',
    'roff': 'application/x-troff',
    't': 'application/x-troff',
    'tr': 'application/x-troff',
    'man': 'application/x-troff-man',
    'me': 'application/x-troff-me',
    'ms': 'application/x-troff-ms',
    # More XML-based
    'xsl': 'application/xml',
    'rdf': 'application/xml',
    'wsdl': 'application/xml',
    'xpdl': 'application/xml',
    # ODF
    'odt': 'application/vnd.oasis.opendocument.text',
    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
    'odp': 'application/vnd.oasis.opendocument.presentation',
    'odg': 'application/vnd.oasis.opendocument.graphics',
    # Fonts
    'otf': 'font/otf',
    'ttf': 'font/ttf',
    'woff': 'font/woff',
    'woff2': 'font/woff2',
    # 3D
    'gltf': 'model/gltf+json',
    'glb': 'model/gltf-binary',
    'stl': 'model/stl',
    # Scripts / Misc
    'sh': 'application/x-sh',
    'php': 'application/x-httpd-php',
    # Code files
    'py': 'text/x-python',  # new (rather than text/plain)
    'c': 'text/plain',  # some prefer text/x-c; we'll keep text/plain
    'h': 'text/plain',
    'ksh': 'text/plain',
    'pl': 'text/plain',
    'bat': 'text/plain',
    # Modern Programming Languages
    'rs': 'text/x-rust',
    'go': 'text/x-go',
    'swift': 'text/x-swift',
    'kt': 'text/x-kotlin',
    'kts': 'text/x-kotlin',
    'java': 'text/x-java-source',
    'scala': 'text/x-scala',
    'rb': 'text/x-ruby',
    'ts': 'text/typescript',
    'tsx': 'text/tsx',
    'jsx': 'text/jsx',
    'vue': 'text/x-vue',
    'dart': 'text/x-dart',
    'lua': 'text/x-lua',
    'r': 'text/x-r',
    'jl': 'text/x-julia',
    'f90': 'text/x-fortran',
    'f95': 'text/x-fortran',
    'f03': 'text/x-fortran',
    'm': 'text/x-objcsrc',  # Objective-C (also MATLAB, but prioritizing Objective-C)
    'cs': 'text/x-csharp',
    'cpp': 'text/x-c++src',
    'cxx': 'text/x-c++src',
    'cc': 'text/x-c++src',
    'hpp': 'text/x-c++hdr',
    'hxx': 'text/x-c++hdr',
    'hh': 'text/x-c++hdr',
    'asm': 'text/x-asm',
    's': 'text/x-asm',
    # Packages etc.
    'apk': 'application/vnd.android.package-archive',
    'deb': 'application/x-debian-package',
    'rpm': 'application/x-rpm',
    # Messages
    'eml': 'message/rfc822',
    'mht': 'message/rfc822',
    'mhtml': 'message/rfc822',
    'nws': 'message/rfc822',
    # Markdown / Markup
    'md': 'text/markdown',
    'markdown': 'text/markdown',
    # RDF-ish / text-ish
    'n3': 'text/n3',
    'rtx': 'text/richtext',
    'rtf': 'text/rtf',
    'srt': 'text/plain',
    'vtt': 'text/vtt',
    'etx': 'text/x-setext',
    'sgm': 'text/x-sgml',
    'sgml': 'text/x-sgml',
    'vcf': 'text/x-vcard',
    # Books
    'epub': 'application/epub+zip',
    # Configuration & Infrastructure Files
    'ini': 'text/plain',
    'conf': 'text/plain',
    'cfg': 'text/plain',
    'config': 'text/plain',
    'properties': 'text/plain',
    'env': 'text/plain',
    'editorconfig': 'text/plain',
    'gitignore': 'text/plain',
    'gitattributes': 'text/plain',
    'dockerignore': 'text/plain',
    'npmrc': 'text/plain',
    'yarnrc': 'text/plain',
    'babelrc': 'application/json',
    'eslintrc': 'application/json',
    'prettierrc': 'application/json',
    # Data Science / Scientific Data Formats
    'parquet': 'application/vnd.apache.parquet',
    'ipynb': 'application/x-ipynb+json',
    'pkl': 'application/octet-stream',  # Python pickle
    'pickle': 'application/octet-stream',  # Python pickle
    'npy': 'application/octet-stream',  # NumPy array
    'npz': 'application/zip',  # NumPy compressed arrays
    'arrow': 'application/vnd.apache.arrow.file',
    'feather': 'application/vnd.apache.arrow.file',  # Apache Arrow IPC format
    'hdf5': 'application/x-hdf5',
    'yaml': 'application/yaml',  # RFC 9512
    'yml': 'application/yaml',
    'toml': 'application/toml',
    'proto': 'text/plain',  # Protocol Buffers definition
    'pb': 'application/octet-stream',  # Protocol Buffers binary
    'avro': 'application/avro',
    'rda': 'application/octet-stream',  # R data
    'rdata': 'application/octet-stream',  # R data
    'rds': 'application/octet-stream',  # R serialized data
    'dta': 'application/x-stata-dta',  # Stata data
    'sas': 'text/x-sas',  # SAS source code
    'sas7bdat': 'application/x-sas-data',  # SAS data
    'sql': 'application/sql',  # SQL (RFC 6922)
    'sav': 'application/x-spss-sav',  # SPSS data
    'mat': 'application/x-matlab-data',  # MATLAB data
    'sqlite': 'application/vnd.sqlite3',  # SQLite database
    'sqlite3': 'application/vnd.sqlite3',
    'db': 'application/vnd.sqlite3',  # Generic database file
    'parq': 'application/vnd.apache.parquet',  # Alternative parquet extension
    # Container & DevOps Formats
    'dockerfile': 'text/plain',
    'tf': 'text/plain',
    'tfvars': 'text/plain',
    'nomad': 'text/plain',
    'hcl': 'text/plain',
    'kubeconfig': 'application/yaml',
    # Build & Package Management
    'gradle': 'text/plain',
    'nuspec': 'application/xml',
    'gemspec': 'text/x-ruby',
    'podspec': 'text/x-ruby',
    'whl': 'application/zip',
    'egg': 'application/zip',
    # Documentation Formats
    'adoc': 'text/asciidoc',
    'asciidoc': 'text/asciidoc',
    'org': 'text/org',
    'bib': 'text/x-bibtex',
    'wiki': 'text/plain',
    'rst': 'text/x-rst',  # reStructuredText
    # Blockchain & Crypto
    'sol': 'text/x-solidity',
    'vy': 'text/x-vyper',
    # Adobe Creative Suite
    'psd': 'image/vnd.adobe.photoshop',
    'psb': 'image/vnd.adobe.photoshop',
    'indd': 'application/x-indesign',
    'idml': 'application/x-indesign',
    'prproj': 'application/x-premiere',
    'aep': 'application/x-aftereffects',
    'xd': 'application/x-xd',
    # CAD & Design Files
    'dwg': 'application/acad',
    'dxf': 'application/dxf',
    'skp': 'application/vnd.sketchup.skp',
    'blend': 'application/x-blender',
    'fbx': 'application/octet-stream',
    'step': 'application/step',
    'stp': 'application/step',
    'iges': 'application/iges',
    'igs': 'application/iges',
    '3ds': 'application/x-3ds',
    'max': 'application/x-3dsmax',
    'c4d': 'application/x-cinema4d',
    # Database & Data Warehouse
    'accdb': 'application/msaccess',
    'mdb': 'application/msaccess',
    'odb': 'application/vnd.oasis.opendocument.database',
    'frm': 'application/octet-stream',
    'myd': 'application/octet-stream',
    'myi': 'application/octet-stream',
    'ibd': 'application/octet-stream',
    # Game Development
    'unity': 'text/plain',
    'unitypackage': 'application/gzip',
    'uasset': 'application/octet-stream',
    'pak': 'application/octet-stream',
    'bsp': 'application/octet-stream',
    # Logs & System Files
    'log': 'text/plain',
    'out': 'text/plain',
    'tmp': 'application/octet-stream',
    'bak': 'application/octet-stream',
    'backup': 'application/octet-stream',
    'cache': 'application/octet-stream',
    'pid': 'text/plain',
    'lock': 'text/plain',
    # Scientific/Academic Formats
    'fits': 'application/fits',
    'fit': 'application/fits',
    'nii': 'application/x-nifti',
    'dcm': 'application/dicom',
    'pdb': 'chemical/x-pdb',
    # Subtitle & Caption Formats
    'ssa': 'text/x-ssa',
    'ass': 'text/x-ssa',  # Advanced SubStation Alpha
    'sub': 'text/x-microdvd',
    'idx': 'application/octet-stream',
}


# Canonical-extension overrides for the few content types whose first-listed
# extension in EXTENSION_TO_CONTENT_TYPE is the less-common alias. Each preferred
# extension is promoted to the front of its reverse-map list so that
# guess_extension() and guess_all_extensions()[0] always agree.
_CANONICAL_OVERRIDES: dict[str, str] = {
    'text/html': 'html',  # not 'htm' (a DOS 8.3 holdover)
    'image/tiff': 'tiff',  # not 'tif'
    'video/mpeg': 'mpeg',  # not 'mpg'
    'application/x-msdownload': 'exe',  # not 'dll'
}

# Well-known non-canonical / legacy MIME spellings mapped to the canonical type this
# library uses. Applied on reverse lookup only (the forward table stays pure), so that
# guess_extension('text/json') resolves the same as 'application/json'. Each value MUST
# be a real type in EXTENSION_TO_CONTENT_TYPE, and no key may itself be a canonical type
# — both are enforced by tests so this table can't silently rot.
_CONTENT_TYPE_ALIASES: dict[str, str] = {
    # JSON
    'text/json': 'application/json',
    # XML — we standardize on application/xml; stdlib and older tools use text/xml
    'text/xml': 'application/xml',
    # JavaScript — application/javascript was the RFC 4329 spelling for years
    'application/javascript': 'text/javascript',
    'application/x-javascript': 'text/javascript',
    # JPEG — image/jpg is a near-universal mistake; image/pjpeg is a legacy IE form
    'image/jpg': 'image/jpeg',
    'image/pjpeg': 'image/jpeg',
    # PNG — legacy
    'image/x-png': 'image/png',
    # Icons — how most favicons are actually served
    'image/x-icon': 'image/vnd.microsoft.icon',
    # SVG — common shorthand for image/svg+xml
    'image/svg': 'image/svg+xml',
    # YAML — application/yaml is RFC 9512 (2024); these predate it
    'application/x-yaml': 'application/yaml',
    'text/yaml': 'application/yaml',
    'text/x-yaml': 'application/yaml',
    # TOML
    'text/toml': 'application/toml',
    # MP3
    'audio/mp3': 'audio/mpeg',
    # ZIP — Windows / IIS commonly send these
    'application/x-zip-compressed': 'application/zip',
    'application/x-zip': 'application/zip',
    # gzip — stdlib and older tools use x-gzip
    'application/x-gzip': 'application/gzip',
    # PDF
    'application/x-pdf': 'application/pdf',
    # CSV
    'application/csv': 'text/csv',
    'text/x-csv': 'text/csv',
    # Markdown — older x- form
    'text/x-markdown': 'text/markdown',
}


@functools.cache
def _reverse_map() -> dict[str, list[str]]:
    """Build the content-type -> extensions reverse of EXTENSION_TO_CONTENT_TYPE.

    Extensions are listed canonical-first: insertion order from the forward dict,
    then adjusted by _CANONICAL_OVERRIDES. The map is built lazily on the first
    reverse lookup and cached for the process lifetime, so importers who only call
    get_content_type() (or the shortcut constants) never pay to construct it.
    """
    reverse: dict[str, list[str]] = {}
    for ext, content_type in EXTENSION_TO_CONTENT_TYPE.items():
        reverse.setdefault(content_type, []).append(ext)

    for content_type, preferred in _CANONICAL_OVERRIDES.items():
        extensions = reverse.get(content_type)
        if extensions and preferred in extensions:
            extensions.remove(preferred)
            extensions.insert(0, preferred)

    return reverse


def _normalize_content_type(content_type: str) -> str:
    """Normalize a MIME type to its canonical lookup key.

    Drops any parameters, trims whitespace, and lowercases, then maps well-known
    non-canonical spellings to the canonical type via _CONTENT_TYPE_ALIASES.

    e.g. '  TEXT/JSON ; charset=utf-8 ' -> 'application/json'
    """
    content_type = content_type.strip()
    if ';' in content_type:
        content_type = content_type.split(';', 1)[0]
    content_type = content_type.strip().lower()
    return _CONTENT_TYPE_ALIASES.get(content_type, content_type)


def guess_extension(content_type: str, with_dot: bool = True) -> Optional[str]:
    """Return the canonical file extension for a MIME / content type.

    This is the reverse of get_content_type(). The lookup is case-insensitive and any
    MIME parameters are ignored, so an HTTP `Content-Type` header value such as
    `text/html; charset=utf-8` resolves the same as `text/html`. Common non-canonical
    or legacy spellings are also accepted — `text/json` resolves like `application/json`
    and `image/jpg` like `image/jpeg`. When a content type maps to several extensions,
    the canonical one is returned (e.g. `image/jpeg` -> `.jpg`); use
    guess_all_extensions() to get every extension.

    The canonical choice follows this library's table and may differ from the standard
    library `mimetypes` module — for example, this returns `.html` for `text/html`.

    Args:
        content_type: A MIME type to look up, optionally with parameters
            (e.g. `application/pdf` or `text/html; charset=utf-8`).
        with_dot: When `True` (default) the returned extension has a leading dot
            (e.g. `.pdf`), which is what you concatenate onto a filename. When `False`
            the bare extension is returned (e.g. `pdf`).

    Returns:
        The canonical extension for the content type, or `None` if it is unknown
        (including empty, whitespace-only, or parameter-only input).

    Raises:
        TypeError: If `content_type` is `None`.

    Example:
        ```python
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
    """

    if content_type is None:
        raise TypeError('content_type cannot be None.')

    extensions = _reverse_map().get(_normalize_content_type(content_type))
    if not extensions:
        return None

    return f'.{extensions[0]}' if with_dot else extensions[0]


def guess_all_extensions(content_type: str, with_dot: bool = True) -> list[str]:
    """Return every known file extension for a MIME / content type, canonical first.

    Like guess_extension(), but returns the full list rather than just the canonical
    extension. The lookup is case-insensitive, MIME parameters are ignored, and common
    non-canonical spellings (e.g. `text/json`, `image/jpg`) resolve to their canonical
    type. The first element always equals guess_extension(content_type). The order
    follows this library's table (canonical first) and is not guaranteed to match the
    standard library `mimetypes` module.

    Args:
        content_type: A MIME type to look up, optionally with parameters
            (e.g. `image/jpeg` or `text/html; charset=utf-8`).
        with_dot: When `True` (default) each extension has a leading dot (e.g. `.jpg`);
            when `False` the bare extensions are returned (e.g. `jpg`).

    Returns:
        A list of extensions, canonical first, or an empty list if the content type is
        unknown (including empty, whitespace-only, or parameter-only input).

    Raises:
        TypeError: If `content_type` is `None`.

    Example:
        ```python
        >>> guess_all_extensions("image/jpeg")
        ['.jpg', '.jpeg', '.jpe']
        >>> guess_all_extensions("text/html")
        ['.html', '.htm']
        >>> guess_all_extensions("application/pdf")
        ['.pdf']
        >>> guess_all_extensions("application/x-does-not-exist")
        []
        ```
    """

    if content_type is None:
        raise TypeError('content_type cannot be None.')

    extensions = _reverse_map().get(_normalize_content_type(content_type), [])
    return [f'.{ext}' for ext in extensions] if with_dot else list(extensions)


class _Unset:
    """Marker type for an omitted ``fallback`` argument.

    Using a private sentinel as the default lets ``get_content_type()`` tell the
    difference between ``fallback`` being left off (use the ``treat_as_binary``
    default) and an explicit ``fallback=None`` (return ``None`` for unknowns).
    """


_UNSET = _Unset()


def get_content_type(
    filename_or_extension: str | Path,
    treat_as_binary: bool = True,
    fallback: Optional[str] | _Unset = _UNSET,
) -> Optional[str]:
    """Return the most specific, commonly accepted MIME type for a filename or extension.

    The lookup is based purely on the extension — the file's bytes are never read. A
    filename, a bare extension (with or without a leading dot), or a `pathlib.Path` are
    all accepted. For URLs, any query string (`?...`) or fragment (`#...`) is stripped
    first; for compound extensions the last segment wins (`archive.tar.gz` resolves as
    `gz`). Matching is case-insensitive.

    Args:
        filename_or_extension: A filename, path, URL, or bare extension to look up.
            Accepts a `str` or a `pathlib.Path`.
        treat_as_binary: Selects the default fallback when the extension is unknown and
            no explicit `fallback` is given. `True` (default) returns
            `application/octet-stream`; `False` returns `text/plain`.
        fallback: An explicit value to return for unknown extensions. When provided, it
            takes precedence over `treat_as_binary`. Pass a MIME type string to override
            the default, or `None` to get `None` back for unknowns (handy when you want to
            branch on a miss rather than receive a placeholder type). When omitted entirely,
            the `treat_as_binary` default is used — so existing callers are unaffected.

    Returns:
        For a known extension, its MIME type; otherwise the explicit `fallback` (which may be `None`) or the default.

    Raises:
        TypeError: If `filename_or_extension` is `None`.

    Example:
        ```python
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
        >>> get_content_type("unknown.xyz", fallback=None) is None
        True
        ```
    """

    if filename_or_extension is None:
        raise TypeError('filename cannot be None.')

    if isinstance(filename_or_extension, Path):
        filename_or_extension = filename_or_extension.suffix

    # Strip query strings and fragments (for URLs)
    # e.g., "file.mp3?cache_id=123" => "file.mp3"
    # e.g., "file.pdf#page=5" => "file.pdf"
    if isinstance(filename_or_extension, str):
        if '?' in filename_or_extension:
            filename_or_extension = filename_or_extension.split('?')[0]
        if '#' in filename_or_extension:
            filename_or_extension = filename_or_extension.split('#')[0]

    if '.' not in filename_or_extension:
        filename_or_extension = f'.{filename_or_extension}'

    # Split by dot, take the last part as extension
    # e.g., "archive.tar.gz" => "gz"
    # Also handle cases like ".webp" => "webp"
    dot_parts = filename_or_extension.lower().split('.')
    ext = dot_parts[-1] if len(dot_parts) > 1 else ''

    if ext in EXTENSION_TO_CONTENT_TYPE:
        return EXTENSION_TO_CONTENT_TYPE[ext]

    if not isinstance(fallback, _Unset):
        return fallback

    return 'application/octet-stream' if treat_as_binary else 'text/plain'


webp: str = get_content_type('.webp')
png: str = get_content_type('.png')
jpg: str = get_content_type('.jpg')
mp3: str = get_content_type('.mp3')
json: str = get_content_type('.json')
pdf: str = get_content_type('.pdf')
zip: str = get_content_type('.zip')  # noqa == it's fine to overwrite zip() in this module only.
xml: str = get_content_type('.xml')
csv: str = get_content_type('.csv')
md: str = get_content_type('.md')
# Data Science
parquet: str = get_content_type('.parquet')
ipynb: str = get_content_type('.ipynb')
pkl: str = get_content_type('.pkl')
yaml: str = get_content_type('.yaml')
toml: str = get_content_type('.toml')
sqlite: str = get_content_type('.sqlite')


def cli() -> None:
    """Look up the MIME type for a filename or extension and print it to stdout.

    Installed as the `content-types` console script (e.g. via `uv tool install
    content-types`). Exits with status 1 if no argument is supplied.

    Example:
        $ content-types my_file.jpg
        image/jpeg
    """
    if len(sys.argv) < 2:
        print('Usage: content-types [FILENAME_OR_EXTENSION]\nExample: content-types .jpg')
        sys.exit(1)

    filename = sys.argv[1]
    mime_type = get_content_type(filename)
    print(mime_type)
