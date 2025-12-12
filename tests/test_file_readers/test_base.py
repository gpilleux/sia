"""
Unit Tests for AbstractFileReader Base Class

Tests coverage:
- Abstract class behavior (cannot instantiate)
- Abstract methods enforcement
- Error hierarchy
- File validation utilities

Domain: Skills (Infrastructure)
Test Level: Unit (no external dependencies)
"""

import tempfile
from abc import ABC
from pathlib import Path

import pytest

from templates.skills.file_readers.base import (AbstractFileReader,
                                                CorruptedFileError,
                                                FileReaderError,
                                                UnsupportedFormatError,
                                                validate_file_exists)


class TestErrorHierarchy:
    """Test exception hierarchy and inheritance."""
    
    def test_file_reader_error_is_exception(self):
        """FileReaderError inherits from Exception."""
        assert issubclass(FileReaderError, Exception)
    
    def test_corrupted_file_error_inherits_from_base(self):
        """CorruptedFileError inherits from FileReaderError."""
        assert issubclass(CorruptedFileError, FileReaderError)
    
    def test_unsupported_format_error_inherits_from_base(self):
        """UnsupportedFormatError inherits from FileReaderError."""
        assert issubclass(UnsupportedFormatError, FileReaderError)
    
    def test_catch_all_error_handling(self):
        """Can catch all errors with FileReaderError."""
        try:
            raise CorruptedFileError("test")
        except FileReaderError as e:
            assert str(e) == "test"
        
        try:
            raise UnsupportedFormatError("test2")
        except FileReaderError as e:
            assert str(e) == "test2"


class TestAbstractFileReader:
    """Test AbstractFileReader abstract class behavior."""
    
    def test_cannot_instantiate_abstract_class(self):
        """Cannot instantiate AbstractFileReader directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            AbstractFileReader()
    
    def test_is_abc_subclass(self):
        """AbstractFileReader is an ABC."""
        assert issubclass(AbstractFileReader, ABC)
    
    def test_has_abstract_methods(self):
        """AbstractFileReader has expected abstract methods."""
        abstract_methods = AbstractFileReader.__abstractmethods__
        assert 'read' in abstract_methods
        assert 'get_extension' in abstract_methods
    
    def test_has_registry_class_attribute(self):
        """AbstractFileReader has registry dict."""
        assert hasattr(AbstractFileReader, 'registry')
        assert isinstance(AbstractFileReader.registry, dict)


class TestConcreteReader:
    """Test concrete reader implementation and registration."""
    
    @pytest.fixture(autouse=True)
    def isolate_registry(self):
        """Isolate registry for each test - save and restore."""
        original_registry = AbstractFileReader.registry.copy()
        AbstractFileReader.registry.clear()
        yield
        # Restore original registry
        AbstractFileReader.registry.clear()
        AbstractFileReader.registry.update(original_registry)
    
    def test_concrete_reader_can_be_instantiated(self):
        """Concrete reader with all methods implemented can be instantiated."""
        
        class TestReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "test"
            
            def read(self, filepath: Path) -> str:
                return "test content"
        
        reader = TestReader()
        assert isinstance(reader, AbstractFileReader)
        assert reader.read(Path("dummy.test")) == "test content"
    
    def test_partial_implementation_cannot_be_instantiated(self):
        """Partial implementation (missing abstract methods) cannot be instantiated."""
        
        class PartialReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "partial"
            # Missing read() implementation
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PartialReader()
    
    def test_supports_method(self):
        """supports() method correctly identifies supported files."""
        
        class TxtReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "txt"
            
            def read(self, filepath: Path) -> str:
                return filepath.read_text()
        
        assert TxtReader.supports(Path("file.txt"))
        assert TxtReader.supports(Path("FILE.TXT"))  # Case insensitive
        assert not TxtReader.supports(Path("file.pdf"))
        assert not TxtReader.supports(Path("file.txt.bak"))


class TestValidateFileExists:
    """Test validate_file_exists utility function."""
    
    def test_valid_file_passes(self):
        """Valid existing file passes validation."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = Path(tmp.name)
        
        try:
            validate_file_exists(tmp_path)  # Should not raise
        finally:
            tmp_path.unlink()
    
    def test_missing_file_raises_file_not_found(self):
        """Missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            validate_file_exists(Path("/nonexistent/file.txt"))
    
    def test_directory_raises_value_error(self):
        """Directory path raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="Path is not a file"):
                validate_file_exists(Path(tmpdir))
    
    def test_unreadable_file_raises_permission_error(self):
        """Unreadable file raises PermissionError."""
        # This test is platform-specific and may be skipped on Windows
        import os
        import sys
        
        if sys.platform == "win32":
            pytest.skip("Permission test not reliable on Windows")
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test")
            tmp_path = Path(tmp.name)
        
        try:
            # Remove read permissions
            os.chmod(tmp_path, 0o000)
            
            with pytest.raises(PermissionError, match="Cannot read file"):
                validate_file_exists(tmp_path)
        finally:
            # Restore permissions before cleanup
            os.chmod(tmp_path, 0o644)
            tmp_path.unlink()


class TestListSupportedFormats:
    """Test list_supported_formats() class method."""
    
    @pytest.fixture(autouse=True)
    def isolate_registry(self):
        """Isolate registry for each test - save and restore."""
        original_registry = AbstractFileReader.registry.copy()
        AbstractFileReader.registry.clear()
        yield
        # Restore original registry
        AbstractFileReader.registry.clear()
        AbstractFileReader.registry.update(original_registry)
    
    def test_empty_registry_returns_empty_list(self):
        """Empty registry returns empty list."""
        assert AbstractFileReader.list_supported_formats() == []
    
    def test_returns_sorted_extensions(self):
        """Returns sorted list of registered extensions."""
        
        class PdfReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "pdf"
            
            def read(self, filepath: Path) -> str:
                return "pdf content"
        
        class TxtReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "txt"
            
            def read(self, filepath: Path) -> str:
                return "txt content"
        
        class DocxReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "docx"
            
            def read(self, filepath: Path) -> str:
                return "docx content"
        
        formats = AbstractFileReader.list_supported_formats()
        assert formats == ["docx", "pdf", "txt"]  # Alphabetically sorted
