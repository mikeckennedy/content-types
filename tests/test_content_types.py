"""
Test suite for content-types library.
Focused on integration tests, spot tests, and negative conditions.
"""

from pathlib import Path

import pytest

import content_types


class TestGetContentType:
    """Test the main get_content_type function."""

    def test_common_image_types(self):
        """Spot test: common image formats work correctly."""
        assert content_types.get_content_type('photo.jpg') == 'image/jpeg'
        assert content_types.get_content_type('image.png') == 'image/png'
        assert content_types.get_content_type('graphic.webp') == 'image/webp'
        assert content_types.get_content_type('animation.gif') == 'image/gif'

    def test_common_document_types(self):
        """Spot test: common document formats."""
        assert content_types.get_content_type('doc.pdf') == 'application/pdf'
        assert (
            content_types.get_content_type('file.docx')
            == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        assert (
            content_types.get_content_type('sheet.xlsx')
            == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    def test_data_science_formats(self):
        """Spot test: data science file formats."""
        assert content_types.get_content_type('data.parquet') == 'application/vnd.apache.parquet'
        assert content_types.get_content_type('notebook.ipynb') == 'application/x-ipynb+json'
        assert content_types.get_content_type('config.yaml') == 'text/yaml'
        assert content_types.get_content_type('config.toml') == 'application/toml'

    def test_video_formats(self):
        """Spot test: video formats."""
        assert content_types.get_content_type('video.mp4') == 'video/mp4'
        assert content_types.get_content_type('movie.mkv') == 'video/x-matroska'
        assert content_types.get_content_type('clip.webm') == 'video/webm'

    def test_audio_formats(self):
        """Spot test: audio formats."""
        assert content_types.get_content_type('song.mp3') == 'audio/mpeg'
        assert content_types.get_content_type('music.flac') == 'audio/flac'
        assert content_types.get_content_type('audio.wav') == 'audio/wav'

    def test_programming_languages(self):
        """Spot test: programming language file extensions."""
        assert content_types.get_content_type('script.py') == 'text/x-python'
        assert content_types.get_content_type('app.js') == 'text/javascript'
        assert content_types.get_content_type('component.tsx') == 'text/tsx'
        assert content_types.get_content_type('main.rs') == 'text/x-rust'
        assert content_types.get_content_type('program.go') == 'text/x-go'

    def test_archive_formats(self):
        """Spot test: archive and compression formats."""
        assert content_types.get_content_type('archive.zip') == 'application/zip'
        assert content_types.get_content_type('backup.tar') == 'application/x-tar'
        assert content_types.get_content_type('compressed.gz') == 'application/gzip'
        assert content_types.get_content_type('file.7z') == 'application/x-7z-compressed'

    def test_path_object_input(self):
        """Integration test: Path objects work correctly."""
        path = Path('document.pdf')
        assert content_types.get_content_type(path) == 'application/pdf'

        path = Path('/some/dir/image.png')
        assert content_types.get_content_type(path) == 'image/png'

    def test_extension_only_input(self):
        """Integration test: can pass just extension with or without dot."""
        assert content_types.get_content_type('.jpg') == 'image/jpeg'
        assert content_types.get_content_type('jpg') == 'image/jpeg'
        assert content_types.get_content_type('.pdf') == 'application/pdf'
        assert content_types.get_content_type('pdf') == 'application/pdf'

    def test_case_insensitive(self):
        """Integration test: extensions are case-insensitive."""
        assert content_types.get_content_type('FILE.JPG') == 'image/jpeg'
        assert content_types.get_content_type('document.PDF') == 'application/pdf'
        assert content_types.get_content_type('.WEBP') == 'image/webp'

    def test_compound_extensions(self):
        """Integration test: compound extensions like .tar.gz."""
        # Should use the last extension
        assert content_types.get_content_type('archive.tar.gz') == 'application/gzip'
        assert content_types.get_content_type('file.tar.bz2') == 'application/x-bzip2'

    def test_unknown_extension_binary_default(self):
        """Negative test: unknown extension defaults to octet-stream."""
        assert content_types.get_content_type('file.xyz123') == 'application/octet-stream'
        assert content_types.get_content_type('unknown.foobar') == 'application/octet-stream'

    def test_unknown_extension_text_mode(self):
        """Negative test: unknown extension with text mode defaults to text/plain."""
        assert content_types.get_content_type('file.xyz123', treat_as_binary=False) == 'text/plain'
        assert content_types.get_content_type('unknown.foobar', treat_as_binary=False) == 'text/plain'

    def test_none_input_raises_exception(self):
        """Negative test: None input raises exception."""
        with pytest.raises(Exception, match='filename cannot be None'):
            content_types.get_content_type(None)

    def test_empty_string(self):
        """Negative test: empty string falls back to default."""
        assert content_types.get_content_type('') == 'application/octet-stream'

    def test_no_extension(self):
        """Negative test: file with no extension."""
        assert content_types.get_content_type('README') == 'application/octet-stream'
        assert content_types.get_content_type('Makefile') == 'application/octet-stream'

    def test_dotfile_extension(self):
        """Negative test: dotfiles are treated as extensions."""
        assert content_types.get_content_type('.gitignore') == 'text/plain'
        assert content_types.get_content_type('.dockerignore') == 'text/plain'


class TestShortcutConstants:
    """Test the shortcut constants provided by the library."""

    def test_common_shortcuts(self):
        """Integration test: common shortcut constants."""
        assert content_types.webp == 'image/webp'
        assert content_types.png == 'image/png'
        assert content_types.jpg == 'image/jpeg'
        assert content_types.mp3 == 'audio/mpeg'
        assert content_types.json == 'application/json'
        assert content_types.pdf == 'application/pdf'
        assert content_types.zip == 'application/zip'
        assert content_types.xml == 'application/xml'
        assert content_types.csv == 'text/csv'
        assert content_types.md == 'text/markdown'

    def test_data_science_shortcuts(self):
        """Integration test: data science shortcut constants."""
        assert content_types.parquet == 'application/vnd.apache.parquet'
        assert content_types.ipynb == 'application/x-ipynb+json'
        assert content_types.pkl == 'application/octet-stream'
        assert content_types.yaml == 'text/yaml'
        assert content_types.toml == 'application/toml'
        assert content_types.sqlite == 'application/vnd.sqlite3'


class TestExtensionToContentTypeDict:
    """Test the EXTENSION_TO_CONTENT_TYPE dictionary."""

    def test_dictionary_exists(self):
        """Spot test: the dictionary is accessible and populated."""
        assert hasattr(content_types, 'EXTENSION_TO_CONTENT_TYPE')
        assert isinstance(content_types.EXTENSION_TO_CONTENT_TYPE, dict)
        assert len(content_types.EXTENSION_TO_CONTENT_TYPE) > 300

    def test_direct_dictionary_access(self):
        """Integration test: can access dictionary directly."""
        assert content_types.EXTENSION_TO_CONTENT_TYPE['jpg'] == 'image/jpeg'
        assert content_types.EXTENSION_TO_CONTENT_TYPE['pdf'] == 'application/pdf'
        assert content_types.EXTENSION_TO_CONTENT_TYPE['parquet'] == 'application/vnd.apache.parquet'

    def test_extensions_without_dots(self):
        """Integration test: dictionary keys don't have dots."""
        # Check that all keys are without leading dots
        for key in content_types.EXTENSION_TO_CONTENT_TYPE.keys():
            assert not key.startswith('.'), f"Extension '{key}' should not start with a dot"


class TestSpecialCases:
    """Test special cases and edge conditions."""

    def test_raw_camera_formats(self):
        """Spot test: RAW camera formats are supported."""
        assert content_types.get_content_type('photo.cr2') == 'image/x-canon-cr2'
        assert content_types.get_content_type('photo.nef') == 'image/x-nikon-nef'
        assert content_types.get_content_type('photo.dng') == 'image/x-adobe-dng'

    def test_modern_web_formats(self):
        """Spot test: modern web formats."""
        assert content_types.get_content_type('image.avif') == 'image/avif'
        assert content_types.get_content_type('audio.opus') == 'audio/opus'
        assert content_types.get_content_type('module.mjs') == 'text/javascript'

    def test_blockchain_formats(self):
        """Spot test: blockchain/smart contract formats."""
        assert content_types.get_content_type('contract.sol') == 'text/x-solidity'
        assert content_types.get_content_type('contract.vy') == 'text/x-vyper'

    def test_config_files(self):
        """Integration test: various config file formats."""
        assert content_types.get_content_type('.env') == 'text/plain'
        assert content_types.get_content_type('.editorconfig') == 'text/plain'
        assert content_types.get_content_type('config.ini') == 'text/plain'
        assert content_types.get_content_type('.babelrc') == 'application/json'

    def test_multiple_dots_in_filename(self):
        """Integration test: filenames with multiple dots."""
        assert content_types.get_content_type('my.file.name.with.dots.jpg') == 'image/jpeg'
        assert content_types.get_content_type('version.1.2.3.tar.gz') == 'application/gzip'


class TestRealWorldScenarios:
    """Integration tests for real-world usage scenarios."""

    def test_web_server_content_type_headers(self):
        """Integration test: simulate setting HTTP headers."""
        files = {
            'index.html': 'text/html',
            'style.css': 'text/css',
            'script.js': 'text/javascript',
            'logo.svg': 'image/svg+xml',
            'data.json': 'application/json',
        }

        for filename, expected_type in files.items():
            content_type = content_types.get_content_type(filename)
            assert content_type == expected_type, f'Failed for {filename}'

    def test_s3_object_metadata(self):
        """Integration test: simulate setting S3 object metadata."""
        s3_objects = [
            Path('uploads/photos/vacation.jpg'),
            Path('data/reports/annual.pdf'),
            Path('backups/db.sqlite'),
            Path('exports/data.parquet'),
        ]

        expected = [
            'image/jpeg',
            'application/pdf',
            'application/vnd.sqlite3',
            'application/vnd.apache.parquet',
        ]

        for path, expected_type in zip(s3_objects, expected):
            assert content_types.get_content_type(path) == expected_type

    def test_batch_file_processing(self):
        """Integration test: process multiple files at once."""
        files = [
            'doc1.pdf',
            'doc2.pdf',
            'doc3.pdf',
            'image1.png',
            'image2.jpg',
            'data.csv',
            'backup.zip',
        ]

        results = [content_types.get_content_type(f) for f in files]

        assert results[0] == results[1] == results[2] == 'application/pdf'
        assert results[3] == 'image/png'
        assert results[4] == 'image/jpeg'
        assert results[5] == 'text/csv'
        assert results[6] == 'application/zip'
