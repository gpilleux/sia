"""
Unit Tests for Registry Auto-Discovery

Tests coverage:
- Auto-registration of concrete readers
- Registry lookup by extension
- get_reader() factory method
- UnsupportedFormatError handling

Domain: Skills (Infrastructure)
Test Level: Unit (no external dependencies)
"""

from pathlib import Path

import pytest

from templates.skills.file_readers.base import (AbstractFileReader,
                                                UnsupportedFormatError)


class TestRegistryAutoDiscovery:
    """Test automatic registration of concrete reader classes."""
    
    @pytest.fixture(autouse=True)
    def isolate_registry(self):
        """Isolate registry for each test - save and restore."""
        original_registry = AbstractFileReader.registry.copy()
        AbstractFileReader.registry.clear()
        yield
        # Restore original registry
        AbstractFileReader.registry.clear()
        AbstractFileReader.registry.update(original_registry)
    
    def test_concrete_class_auto_registers(self):
        """Concrete reader class automatically registers in registry."""
        
        class TestReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "test"
            
            def read(self, filepath: Path) -> str:
                return "test content"
        
        # Check registration happened automatically
        assert "test" in AbstractFileReader.registry
        assert AbstractFileReader.registry["test"] == TestReader
    
    def test_abstract_class_does_not_register(self):
        """Abstract class (missing implementation) does NOT register."""
        
        class PartialReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "partial"
            # Missing read() implementation
        
        # Internal registry may contain it, but it should be filtered out
        # when accessing concrete classes
        assert "partial" not in AbstractFileReader._get_concrete_registry()
        
        # Verify it's not accessible via list_supported_formats()
        assert "partial" not in AbstractFileReader.list_supported_formats()
        
        # Verify get_reader() raises error for this extension
        with pytest.raises(UnsupportedFormatError):
            AbstractFileReader.get_reader(Path("file.partial"))
    
    def test_multiple_readers_register_independently(self):
        """Multiple concrete readers register with different extensions."""
        
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
        
        assert "txt" in AbstractFileReader.registry
        assert "pdf" in AbstractFileReader.registry
        assert AbstractFileReader.registry["txt"] == TxtReader
        assert AbstractFileReader.registry["pdf"] == PdfReader
    
    def test_registry_is_class_level_shared(self):
        """Registry is shared across all instances (class-level attribute)."""
        
        class Reader1(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "r1"
            
            def read(self, filepath: Path) -> str:
                return "r1"
        
        class Reader2(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "r2"
            
            def read(self, filepath: Path) -> str:
                return "r2"
        
        # All classes share the same registry
        assert Reader1.registry is Reader2.registry
        assert Reader1.registry is AbstractFileReader.registry
        assert len(AbstractFileReader.registry) == 2


class TestGetReaderFactory:
    """Test get_reader() factory method."""
    
    @pytest.fixture(autouse=True)
    def isolate_registry(self):
        """Isolate registry for each test - save and restore."""
        original_registry = AbstractFileReader.registry.copy()
        AbstractFileReader.registry.clear()
        yield
        # Restore original registry
        AbstractFileReader.registry.clear()
        AbstractFileReader.registry.update(original_registry)
    
    @pytest.fixture
    def sample_readers(self):
        """Create sample readers for testing."""
        
        class TxtReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "txt"
            
            def read(self, filepath: Path) -> str:
                return filepath.read_text()
        
        class PdfReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "pdf"
            
            def read(self, filepath: Path) -> str:
                return "pdf content"
        
        return {"txt": TxtReader, "pdf": PdfReader}
    
    def test_get_reader_returns_correct_instance(self, sample_readers):
        """get_reader() returns instance of correct reader class."""
        reader = AbstractFileReader.get_reader(Path("document.txt"))
        assert isinstance(reader, sample_readers["txt"])
        
        reader = AbstractFileReader.get_reader(Path("report.pdf"))
        assert isinstance(reader, sample_readers["pdf"])
    
    def test_get_reader_case_insensitive(self, sample_readers):
        """get_reader() handles case-insensitive extensions."""
        reader_lower = AbstractFileReader.get_reader(Path("file.txt"))
        reader_upper = AbstractFileReader.get_reader(Path("file.TXT"))
        reader_mixed = AbstractFileReader.get_reader(Path("file.Txt"))
        
        assert type(reader_lower) == type(reader_upper) == type(reader_mixed)
        assert isinstance(reader_lower, sample_readers["txt"])
    
    def test_get_reader_unsupported_format_raises(self):
        """get_reader() raises UnsupportedFormatError for unknown extension."""
        
        class TxtReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "txt"
            
            def read(self, filepath: Path) -> str:
                return "txt"
        
        with pytest.raises(UnsupportedFormatError) as exc_info:
            AbstractFileReader.get_reader(Path("file.unknown"))
        
        error_msg = str(exc_info.value)
        assert "Unsupported file format: '.unknown'" in error_msg
        assert "Supported formats: txt" in error_msg
    
    def test_get_reader_error_message_lists_supported_formats(self, sample_readers):
        """Error message lists all supported formats."""
        with pytest.raises(UnsupportedFormatError) as exc_info:
            AbstractFileReader.get_reader(Path("file.docx"))
        
        error_msg = str(exc_info.value)
        assert "pdf" in error_msg
        assert "txt" in error_msg
    
    def test_get_reader_handles_no_extension(self):
        """get_reader() handles files with no extension."""
        with pytest.raises(UnsupportedFormatError) as exc_info:
            AbstractFileReader.get_reader(Path("README"))
        
        # Empty extension should be in error
        assert "Unsupported file format: ''" in str(exc_info.value)
    
    def test_get_reader_handles_multiple_dots(self, sample_readers):
        """get_reader() uses only the final extension."""
        reader = AbstractFileReader.get_reader(Path("archive.tar.txt"))
        assert isinstance(reader, sample_readers["txt"])
        
        reader = AbstractFileReader.get_reader(Path("report.2024.pdf"))
        assert isinstance(reader, sample_readers["pdf"])


class TestRegistryIntegration:
    """Integration tests for complete registry workflow."""
    
    @pytest.fixture(autouse=True)
    def isolate_registry(self):
        """Isolate registry for each test - save and restore."""
        original_registry = AbstractFileReader.registry.copy()
        AbstractFileReader.registry.clear()
        yield
        # Restore original registry
        AbstractFileReader.registry.clear()
        AbstractFileReader.registry.update(original_registry)
    
    def test_end_to_end_workflow(self):
        """Test complete workflow: define reader → auto-register → get_reader → use."""
        
        # Step 1: Define reader (auto-registers)
        class JsonReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "json"
            
            def read(self, filepath: Path) -> str:
                return '{"test": "data"}'
        
        # Step 2: Verify registration
        assert "json" in AbstractFileReader.registry
        
        # Step 3: Get reader via factory
        reader = AbstractFileReader.get_reader(Path("config.json"))
        
        # Step 4: Use reader
        assert isinstance(reader, JsonReader)
        result = reader.read(Path("config.json"))
        assert result == '{"test": "data"}'
    
    def test_registry_survives_instance_creation(self):
        """Registry persists across instance creation and deletion."""
        
        class TempReader(AbstractFileReader):
            @classmethod
            def get_extension(cls) -> str:
                return "tmp"
            
            def read(self, filepath: Path) -> str:
                return "temp"
        
        # Create and delete instance
        reader1 = TempReader()
        del reader1
        
        # Registry should still have the class
        assert "tmp" in AbstractFileReader.registry
        
        # Can still create new instances
        reader2 = AbstractFileReader.get_reader(Path("file.tmp"))
        assert isinstance(reader2, TempReader)
