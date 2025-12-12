"""
Unit Tests for Error Handling

Tests coverage:
- FileReaderError base exception
- CorruptedFileError handling
- UnsupportedFormatError handling
- validate_file_exists edge cases

Domain: Skills (Infrastructure)
Test Level: Unit (no external dependencies)
"""

import tempfile
from pathlib import Path

import pytest

from templates.skills.file_readers.base import (AbstractFileReader,
                                                CorruptedFileError,
                                                FileReaderError,
                                                UnsupportedFormatError,
                                                validate_file_exists)


class TestFileReaderErrorUsage:
    """Test FileReaderError as catch-all exception."""
    
    def test_can_catch_all_reader_errors(self):
        """FileReaderError catches all reader-specific exceptions."""
        errors = [
            CorruptedFileError("corrupted"),
            UnsupportedFormatError("unsupported"),
            FileReaderError("generic"),
        ]
        
        for error in errors:
            try:
                raise error
            except FileReaderError as e:
                # All should be caught
                assert isinstance(e, FileReaderError)
    
    def test_error_messages_preserved(self):
        """Error messages are preserved when caught."""
        custom_message = "Custom error message with details"
        
        try:
            raise CorruptedFileError(custom_message)
        except FileReaderError as e:
            assert str(e) == custom_message


class TestCorruptedFileErrorScenarios:
    """Test CorruptedFileError in realistic scenarios."""
    
    @pytest.fixture(autouse=True)
    def isolate_registry(self):
        """Isolate registry for each test - save and restore."""
        original_registry = AbstractFileReader.registry.copy()
        AbstractFileReader.registry.clear()
        yield
        # Restore original registry
        AbstractFileReader.registry.clear()
        AbstractFileReader.registry.update(original_registry)
    
    def test_reader_raises_corrupted_error_for_invalid_file(self):
        """Reader can raise CorruptedFileError for invalid files."""
        
        class StrictReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "strict"
            
            def read(self, filepath: Path) -> str:
                content = filepath.read_bytes()
                if not content.startswith(b"VALID"):
                    raise CorruptedFileError(
                        f"Invalid file header: {filepath.name}"
                    )
                return content.decode('utf-8')
        
        # Create invalid file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.strict', delete=False) as tmp:
            tmp.write(b"INVALID DATA")
            tmp_path = Path(tmp.name)
        
        try:
            reader = StrictReader()
            with pytest.raises(CorruptedFileError, match="Invalid file header"):
                reader.read(tmp_path)
        finally:
            tmp_path.unlink()
    
    def test_corrupted_error_provides_context(self):
        """CorruptedFileError should provide helpful context."""
        
        class DetailedReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "detailed"
            
            def read(self, filepath: Path) -> str:
                try:
                    content = filepath.read_text(encoding='utf-8')
                    if len(content) == 0:
                        raise CorruptedFileError(
                            f"File is empty: {filepath.name}"
                        )
                    return content
                except UnicodeDecodeError as e:
                    raise CorruptedFileError(
                        f"Invalid UTF-8 encoding in {filepath.name}: {e}"
                    ) from e
        
        # Test empty file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.detailed', delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        try:
            reader = DetailedReader()
            with pytest.raises(CorruptedFileError, match="File is empty"):
                reader.read(tmp_path)
        finally:
            tmp_path.unlink()


class TestUnsupportedFormatErrorMessages:
    """Test UnsupportedFormatError provides helpful messages."""
    
    @pytest.fixture(autouse=True)
    def isolate_registry(self):
        """Isolate registry for each test - save and restore."""
        original_registry = AbstractFileReader.registry.copy()
        AbstractFileReader.registry.clear()
        yield
        # Restore original registry
        AbstractFileReader.registry.clear()
        AbstractFileReader.registry.update(original_registry)
    
    def test_error_lists_supported_formats(self):
        """Error message lists all supported formats."""
        
        class TxtReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "txt"
            
            def read(self, filepath: Path) -> str:
                return "txt"
        
        class PdfReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "pdf"
            
            def read(self, filepath: Path) -> str:
                return "pdf"
        
        with pytest.raises(UnsupportedFormatError) as exc_info:
            AbstractFileReader.get_reader(Path("file.docx"))
        
        error_msg = str(exc_info.value)
        assert "Unsupported file format: '.docx'" in error_msg
        assert "pdf, txt" in error_msg  # Sorted list
    
    def test_error_with_no_readers_registered(self):
        """Error message when no readers are registered."""
        with pytest.raises(UnsupportedFormatError) as exc_info:
            AbstractFileReader.get_reader(Path("file.any"))
        
        error_msg = str(exc_info.value)
        assert "Unsupported file format: '.any'" in error_msg
        assert "Supported formats:" in error_msg


class TestValidateFileExistsEdgeCases:
    """Test validate_file_exists utility with edge cases."""
    
    def test_validates_normal_file(self):
        """Normal readable file passes validation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("test content")
            tmp_path = Path(tmp.name)
        
        try:
            validate_file_exists(tmp_path)  # Should not raise
        finally:
            tmp_path.unlink()
    
    def test_empty_file_passes(self):
        """Empty file (0 bytes) still passes validation."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        try:
            validate_file_exists(tmp_path)  # Should not raise
        finally:
            tmp_path.unlink()
    
    def test_nonexistent_file_fails(self):
        """Nonexistent file raises FileNotFoundError."""
        fake_path = Path("/tmp/nonexistent_file_12345.txt")
        with pytest.raises(FileNotFoundError, match="File not found"):
            validate_file_exists(fake_path)
    
    def test_directory_fails(self):
        """Directory path raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="Path is not a file"):
                validate_file_exists(Path(tmpdir))
    
    def test_symlink_to_file_passes(self):
        """Symlink to valid file passes validation."""
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("content")
            tmp_path = Path(tmp.name)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            link_path = Path(tmpdir) / "link.txt"
            try:
                os.symlink(tmp_path, link_path)
                validate_file_exists(link_path)  # Should not raise
            finally:
                tmp_path.unlink()
    
    def test_broken_symlink_fails(self):
        """Broken symlink raises FileNotFoundError."""
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            link_path = Path(tmpdir) / "broken_link.txt"
            target_path = Path(tmpdir) / "nonexistent_target.txt"
            
            os.symlink(target_path, link_path)
            
            with pytest.raises(FileNotFoundError):
                validate_file_exists(link_path)


class TestErrorHandlingIntegration:
    """Integration tests for complete error handling workflow."""
    
    @pytest.fixture(autouse=True)
    def isolate_registry(self):
        """Isolate registry for each test - save and restore."""
        original_registry = AbstractFileReader.registry.copy()
        AbstractFileReader.registry.clear()
        yield
        # Restore original registry
        AbstractFileReader.registry.clear()
        AbstractFileReader.registry.update(original_registry)
    
    def test_reader_with_full_error_handling(self):
        """Reader with comprehensive error handling."""
        
        class SafeReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "safe"
            
            def read(self, filepath: Path) -> str:
                # Validate file exists
                validate_file_exists(filepath)
                
                # Read with error handling
                try:
                    content = filepath.read_text(encoding='utf-8')
                except UnicodeDecodeError as e:
                    raise CorruptedFileError(
                        f"File has invalid UTF-8 encoding: {e}"
                    ) from e
                
                # Validate content
                if len(content.strip()) == 0:
                    raise CorruptedFileError("File is empty or contains only whitespace")
                
                return content
        
        # Test valid file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.safe', delete=False) as tmp:
            tmp.write("Valid content")
            tmp_path = Path(tmp.name)
        
        try:
            reader = SafeReader()
            result = reader.read(tmp_path)
            assert result == "Valid content"
        finally:
            tmp_path.unlink()
        
        # Test empty file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.safe', delete=False) as tmp:
            tmp.write("   \n\t  ")  # Only whitespace
            tmp_path = Path(tmp.name)
        
        try:
            reader = SafeReader()
            with pytest.raises(CorruptedFileError, match="empty or contains only whitespace"):
                reader.read(tmp_path)
        finally:
            tmp_path.unlink()
        
        # Test nonexistent file
        reader = SafeReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/tmp/nonexistent_12345.safe"))
    
    def test_error_hierarchy_allows_granular_catching(self):
        """Can catch specific errors or use base exception."""
        
        class MultiErrorReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "multi"
            
            def read(self, filepath: Path) -> str:
                content = filepath.read_text()
                if "CORRUPT" in content:
                    raise CorruptedFileError("Corrupted marker found")
                if "ERROR" in content:
                    raise FileReaderError("Generic error marker found")
                return content
        
        reader = MultiErrorReader()
        
        # Test specific error catching
        with tempfile.NamedTemporaryFile(mode='w', suffix='.multi', delete=False) as tmp:
            tmp.write("CORRUPT data")
            tmp_path = Path(tmp.name)
        
        try:
            caught_specific = False
            try:
                reader.read(tmp_path)
            except CorruptedFileError:
                caught_specific = True
            
            assert caught_specific
        finally:
            tmp_path.unlink()
        
        # Test base error catching
        with tempfile.NamedTemporaryFile(mode='w', suffix='.multi', delete=False) as tmp:
            tmp.write("ERROR data")
            tmp_path = Path(tmp.name)
        
        try:
            caught_base = False
            try:
                reader.read(tmp_path)
            except FileReaderError:
                caught_base = True
            
            assert caught_base
        finally:
            tmp_path.unlink()
