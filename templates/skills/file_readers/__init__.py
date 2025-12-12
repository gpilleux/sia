"""
File Readers Module - Public API

Exports:
    Base Classes and Errors:
    - AbstractFileReader: Base class for implementing new readers
    - FileReaderError: Base exception class
    - CorruptedFileError: Raised for corrupted/invalid files
    - UnsupportedFormatError: Raised for unsupported file extensions
    - validate_file_exists: Utility function for file validation
    
    Concrete Readers:
    - DocxReader: Microsoft Word documents (.docx)
    - XlsxReader: Microsoft Excel spreadsheets (.xlsx)
    - PdfReader: Portable Document Format (.pdf)

Usage:
    >>> from file_readers import AbstractFileReader
    >>> reader = AbstractFileReader.get_reader(Path("document.pdf"))
    >>> text = reader.read(Path("document.pdf"))
    
    >>> # Or use concrete readers directly
    >>> from file_readers import PdfReader
    >>> reader = PdfReader()
    >>> text = reader.read(Path("document.pdf"))
"""

from .base import (AbstractFileReader, CorruptedFileError, FileReaderError,
                   UnsupportedFormatError, validate_file_exists)
# Import concrete readers to trigger auto-registration
from .docx_reader import DocxReader
from .pdf_reader import PdfReader
from .xlsx_reader import XlsxReader

__all__ = [
    # Base classes and errors
    'AbstractFileReader',
    'FileReaderError',
    'CorruptedFileError',
    'UnsupportedFormatError',
    'validate_file_exists',
    # Concrete readers
    'DocxReader',
    'XlsxReader',
    'PdfReader',
]

__version__ = '1.0.0'
