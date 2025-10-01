import sys
from pathlib import Path
from typing import Dict

__VERSION__ = '0.3.0'

# This dictionary maps file extensions (no dot) to the most specific content type.

# noinspection SpellCheckingInspection
EXTENSION_TO_CONTENT_TYPE: Dict[str, str] = {
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
    'ass': 'audio/aac',
    'adts': 'audio/aac',
    'rst': 'text/x-rst',
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
    'yaml': 'text/yaml',
    'yml': 'text/yaml',
    'toml': 'application/toml',
    'proto': 'text/plain',  # Protocol Buffers definition
    'pb': 'application/octet-stream',  # Protocol Buffers binary
    'avro': 'application/avro',
    'rda': 'application/octet-stream',  # R data
    'rdata': 'application/octet-stream',  # R data
    'rds': 'application/octet-stream',  # R serialized data
    'dta': 'application/x-stata-dta',  # Stata data
    'sas7bdat': 'application/x-sas-data',  # SAS data
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
    'kubeconfig': 'text/yaml',
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
    'sub': 'text/x-microdvd',
    'idx': 'application/octet-stream',
}


def get_content_type(filename_or_extension: str | Path, treat_as_binary: bool = True) -> str:
    """
    Given a filename (or just an extension), return the most specific,
    commonly accepted MIME type based on extension.

    Falls back to 'application/octet-stream' if `treat_as_binary` is True (default) and 'text/plain' if it is
    False when the extension is not known.

    Example:
        >>> get_content_type("picture.jpg")
        'image/jpeg'
        >>> get_content_type(".webp")
        'image/webp'
        >>> get_content_type("script.js")
        'application/javascript'
        >>> get_content_type("unknown.xyz")
        'application/octet-stream'
        >>> get_content_type("unknown.xyz", treat_as_binary=False)
        'text/plain'
    """

    if filename_or_extension is None:
        raise Exception('filename cannot be None.')

    if isinstance(filename_or_extension, Path):
        filename_or_extension = filename_or_extension.suffix

    if '.' not in filename_or_extension:
        filename_or_extension = f'.{filename_or_extension}'

    # Split by dot, take the last part as extension
    # e.g., "archive.tar.gz" => "gz"
    # Also handle cases like ".webp" => "webp"
    dot_parts = filename_or_extension.lower().split('.')
    ext = dot_parts[-1] if len(dot_parts) > 1 else ''

    if treat_as_binary:
        return EXTENSION_TO_CONTENT_TYPE.get(ext, 'application/octet-stream')

    return EXTENSION_TO_CONTENT_TYPE.get(ext, 'text/plain')


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


def cli():
    """
    A simple CLI to look up the MIME type for a given filename or extension.
    Install via uv tool install content-types
    Usage example :
        content-types my_file.jpg
    """
    if len(sys.argv) < 2:
        print('Usage: contenttypes [FILENAME_OR_EXTENSION]\nExample: contenttypes .jpg')
        sys.exit(1)

    filename = sys.argv[1]
    mime_type = get_content_type(filename)
    print(mime_type)
