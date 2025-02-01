import sys
from pathlib import Path
from typing import Dict

__VERSION__ = '0.2.3'

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
    'c': 'text/plain',  # some prefer text/x-c; we’ll keep text/plain
    'h': 'text/plain',
    'ksh': 'text/plain',
    'pl': 'text/plain',
    'bat': 'text/plain',
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
}


def get_content_type(filename_or_extension: str | Path, treat_as_binary: bool = True) -> str:
    """
    Given a filename (or just an extension), return the most specific,
    commonly accepted MIME type based on extension.

    Falls back to 'application/octet-stream' if not found.

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
        'application/octet-stream'
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


def cli():
    """
    A simple CLI to look up the MIME type for a given filename or extension.
    Usage example:
        contenttypes my_file.jpg
    """
    if len(sys.argv) < 2:
        print('Usage: contenttypes [FILENAME_OR_EXTENSION]\nExample: contenttypes .jpg')
        sys.exit(1)

    filename = sys.argv[1]
    mime_type = get_content_type(filename)
    print(mime_type)
