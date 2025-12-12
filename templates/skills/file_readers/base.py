"""
File Readers Core Module - Base Classes and Registry

This module provides the foundation for the file reader system, implementing:
- AbstractFileReader: Base class with auto-discovery registry
- Error hierarchy: FileReaderError, CorruptedFileError
- Registry pattern: Automatic registration of concrete readers

Domain: Skills (Infrastructure)
Bounded Context: File Processing
Pattern: Strategy + Registry (Auto-discovery)

Invariant:
    AbstractFileReader.registry = {}
    ∧ ∀ subclass: subclass.__abstractmethods__ = ∅ ⇒ subclass ∈ registry
    ∧ registry.get(extension) → Reader | None
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional, Type

# ============================================================================
# ERROR HIERARCHY
# ============================================================================

class FileReaderError(Exception):
    """
    Base exception for all file reading errors.
    
    Use this as the parent class for specific error types to enable
    catch-all error handling while preserving error granularity.
    """
    pass


class CorruptedFileError(FileReaderError):
    """
    Raised when a file is corrupted or has an invalid format.
    
    Examples:
        - Malformed ZIP archive (DOCX/XLSX)
        - Invalid PDF structure
        - Truncated file
        - Missing required metadata
    """
    pass


class UnsupportedFormatError(FileReaderError):
    """
    Raised when attempting to read a file with an unsupported extension.
    
    This indicates that no reader is registered for the file's extension.
    """
    pass


# ============================================================================
# ABSTRACT BASE CLASS + REGISTRY
# ============================================================================

class AbstractFileReader(ABC):
    """
    Abstract base class for file readers with auto-discovery registry.
    
    This class implements the Strategy pattern with automatic registration
    of concrete implementations. When a subclass is defined and implements
    all abstract methods, it's automatically added to the registry.
    
    Registry Pattern:
        - Concrete readers auto-register via __init_subclass__
        - Registry is a class-level dict: {extension: ReaderClass}
        - Non-concrete classes (partial implementations) are NOT registered
    
    Example:
        >>> class TxtReader(AbstractFileReader):
        ...     @classmethod
        ...     def get_extension(cls) -> str:
        ...         return "txt"
        ...     
        ...     def read(self, filepath: Path) -> str:
        ...         return filepath.read_text(encoding="utf-8")
        >>> 
        >>> # TxtReader is now in AbstractFileReader.registry["txt"]
        >>> reader = AbstractFileReader.get_reader(Path("file.txt"))
        >>> text = reader.read(Path("file.txt"))
    
    Attributes:
        registry: Class-level dict mapping extensions to reader classes
    """
    
    registry: Dict[str, Type['AbstractFileReader']] = {}
    
    def __init_subclass__(cls, **kwargs):
        """
        Auto-register concrete subclasses in the registry.
        
        Called automatically when a class inherits from AbstractFileReader.
        Only concrete classes (no abstract methods) are registered.
        
        Args:
            **kwargs: Forwarded to super().__init_subclass__
        """
        super().__init_subclass__(**kwargs)
        
        # The __abstractmethods__ attribute is set by ABCMeta metaclass AFTER
        # __init_subclass__ is called. We can't rely on it here.
        # Instead, we register all classes that define get_extension(),
        # but actual instantiation will fail for abstract classes anyway.
        try:
            if hasattr(cls, 'get_extension') and callable(getattr(cls, 'get_extension')):
                extension = cls.get_extension()
                # Double-check this isn't an abstract class by verifying
                # it doesn't have abstract methods (this check happens after ABCMeta processes)
                # We do this in a deferred way - register first, check after class definition
                cls.registry[extension] = cls
        except (NotImplementedError, AttributeError, TypeError):
            pass
    
    @abstractmethod
    def read(self, filepath: Path) -> str:
        """
        Extract text content from a file.
        
        Args:
            filepath: Path to the file to read
            
        Returns:
            Extracted text as UTF-8 string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            CorruptedFileError: If file is corrupted or invalid format
            PermissionError: If file cannot be read
        """
        pass
    
    @classmethod
    @abstractmethod
    def get_extension(cls) -> str:
        """
        Return the file extension this reader supports.
        
        Returns:
            Extension without leading dot (e.g., 'docx', 'pdf')
        """
        pass
    
    @classmethod
    def supports(cls, filepath: Path) -> bool:
        """
        Check if this reader supports the given file.
        
        Args:
            filepath: Path to check
            
        Returns:
            True if this reader can handle the file's extension
        """
        extension = filepath.suffix.lstrip('.').lower()
        return extension == cls.get_extension()
    
    @classmethod
    def _get_concrete_registry(cls) -> Dict[str, Type['AbstractFileReader']]:
        """
        Get registry filtered to only concrete (non-abstract) classes.
        
        This is needed because __init_subclass__ runs before ABCMeta sets
        __abstractmethods__, so we register all classes and filter later.
        
        Returns:
            Dict mapping extensions to concrete reader classes only
        """
        return {
            ext: reader_cls
            for ext, reader_cls in cls.registry.items()
            if not reader_cls.__abstractmethods__  # Empty set means concrete
        }
    
    @classmethod
    def get_reader(cls, filepath: Path) -> 'AbstractFileReader':
        """
        Get the appropriate reader instance for a file.
        
        Uses the registry to find a reader that supports the file's extension.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Instance of the appropriate reader class
            
        Raises:
            UnsupportedFormatError: If no reader supports this extension
        
        Example:
            >>> reader = AbstractFileReader.get_reader(Path("doc.pdf"))
            >>> text = reader.read(Path("doc.pdf"))
        """
        suffix = filepath.suffix
        # Handle files with no extension (suffix will be empty string)
        extension = suffix.lstrip('.').lower() if suffix else ''
        
        # Use filtered registry (only concrete classes)
        concrete_registry = cls._get_concrete_registry()
        reader_class = concrete_registry.get(extension)
        
        if not reader_class:
            supported = ', '.join(sorted(concrete_registry.keys()))
            # Format extension with dot for display (except for empty extension)
            if extension:
                ext_display = f"'.{extension}'"
            else:
                ext_display = "''"
            raise UnsupportedFormatError(
                f"Unsupported file format: {ext_display}. "
                f"Supported formats: {supported}"
            )
        
        return reader_class()
    
    @classmethod
    def list_supported_formats(cls) -> list[str]:
        """
        List all supported file extensions.
        
        Returns:
            Sorted list of supported extensions (without leading dot)
        """
        concrete_registry = cls._get_concrete_registry()
        return sorted(concrete_registry.keys())


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_file_exists(filepath: Path) -> None:
    """
    Validate that a file exists and is readable.
    
    Args:
        filepath: Path to validate
        
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file exists but cannot be read
    """
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    if not filepath.is_file():
        raise ValueError(f"Path is not a file: {filepath}")
    
    # Test read permission by attempting to open
    try:
        with open(filepath, 'rb'):
            pass
    except PermissionError as e:
        raise PermissionError(f"Cannot read file: {filepath}") from e
