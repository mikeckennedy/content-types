import sys
from pathlib import Path
from typing import Dict

__VERSION__ = '0.2.1'

# This dictionary maps file extensions (no dot) to the most specific content type.
EXTENSION_TO_CONTENT_TYPE: Dict[str, str] = {
    # Text
    'txt': 'text/plain',
    'htm': 'text/html',
    'html': 'text/html',
    'css': 'text/css',
    'csv': 'text/csv',
    'tsv': 'text/tab-separated-values',
    # JavaScript
    'js': 'application/javascript',  # commonly "application/javascript" nowadays
    # JSON
    'json': 'application/json',
    'map': 'application/json',  # e.g., SourceMap
    # XML
    'xml': 'application/xml',  # can also be "text/xml" in some contexts
    # Images
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'webp': 'image/webp',
    'avif': 'image/avif',
    'ico': 'image/x-icon',  # sometimes "image/vnd.microsoft.icon"
    'svg': 'image/svg+xml',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    # Audio
    'mp3': 'audio/mpeg',
    'ogg': 'audio/ogg',
    'wav': 'audio/wav',
    'aac': 'audio/aac',
    'flac': 'audio/flac',
    'm4a': 'audio/mp4',
    'weba': 'audio/webm',
    # Video
    'mp4': 'video/mp4',
    'm4v': 'video/mp4',  # often container-based
    'mov': 'video/quicktime',
    'avi': 'video/x-msvideo',
    'wmv': 'video/x-ms-wmv',
    'mpg': 'video/mpeg',
    'mpeg': 'video/mpeg',
    'ogv': 'video/ogg',
    'webm': 'video/webm',
    # Application / Archive
    'pdf': 'application/pdf',
    'zip': 'application/zip',
    'gz': 'application/gzip',
    'tgz': 'application/gzip',  # or "application/x-tar" + "gzip"
    'tar': 'application/x-tar',
    '7z': 'application/x-7z-compressed',
    'rar': 'application/vnd.rar',
    # Office
    'doc': 'application/msword',
    'xls': 'application/vnd.ms-excel',
    'ppt': 'application/vnd.ms-powerpoint',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    # OpenDocument
    'odt': 'application/vnd.oasis.opendocument.text',
    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
    'odp': 'application/vnd.oasis.opendocument.presentation',
    'odg': 'application/vnd.oasis.opendocument.graphics',
    # Fonts
    'otf': 'font/otf',
    'ttf': 'font/ttf',
    'woff': 'font/woff',
    'woff2': 'font/woff2',
    # 3D model
    'gltf': 'model/gltf+json',
    'glb': 'model/gltf-binary',
    'stl': 'model/stl',
    'obj': 'model/obj',  # not officially registered; widely used
    # Scripts / misc
    'sh': 'application/x-sh',
    'php': 'application/x-httpd-php',  # Usually not used at runtime for real responses
    'exe': 'application/x-msdownload',
    # Misc
    'apk': 'application/vnd.android.package-archive',
    'deb': 'application/x-debian-package',
    'rpm': 'application/x-rpm',
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
