"""
PDF File Reader - Portable Document Format Parser

Extracts text from PDF files including:
- All pages in document order
- Text blocks sorted for natural reading order
- Page separators for multi-page documents

Domain: Skills (Infrastructure)
Bounded Context: File Processing
Pattern: Strategy (concrete implementation)

Dependencies:
    - PyMuPDF (fitz): High-performance PDF library
    
Invariant:
    PdfReader.read(valid_pdf) → non_empty_text
    ∧ PdfReader.read(corrupted_pdf) → CorruptedFileError
    ∧ PdfReader ∈ AbstractFileReader.registry["pdf"]

REQ-011: File Reader Skills System
QUANT-011-003: Concrete Readers Implementation
"""

from pathlib import Path
from typing import TYPE_CHECKING

from .base import AbstractFileReader, CorruptedFileError, validate_file_exists

if TYPE_CHECKING:
    import pymupdf


class PdfReader(AbstractFileReader):
    """
    Extract text from PDF (Portable Document Format) files.
    
    This reader uses PyMuPDF (fitz) to extract text from PDF files,
    preserving natural reading order and handling various PDF types.
    
    Features:
        - Natural reading order (left-to-right, top-to-bottom)
        - Page-by-page extraction with markers
        - Support for multi-column layouts
        - Efficient memory usage
    
    Implementation Notes:
        - Uses get_text("text", sort=True) for sorted block extraction
        - sort=True ensures natural reading order (critical for multi-column)
        - Document properly closed after reading
        - Empty pages are skipped
    
    Edge Cases Handled:
        - Corrupted PDF structure (FileDataError)
        - Password-protected PDFs (detected, clear error message)
        - Scanned PDFs without OCR (returns empty or sparse text)
        - Empty pages (skipped)
        - Invalid PDF headers
    
    Limitations:
        - Password-protected PDFs require password parameter (not implemented)
        - Scanned PDFs without embedded text return empty strings
        - Images and graphics are ignored (text extraction only)
        - Form fields may not be extracted properly
    
    Example:
        >>> reader = PdfReader()
        >>> text = reader.read(Path("document.pdf"))
        >>> print(text[:200])
    """
    
    @classmethod
    def get_extension(cls) -> str:
        """Return supported extension: 'pdf'"""
        return "pdf"
    
    def read(self, filepath: Path) -> str:
        """
        Extract all text from a PDF file.
        
        Args:
            filepath: Path to PDF file
            
        Returns:
            Extracted text with page sections and natural reading order
            
        Raises:
            FileNotFoundError: If file doesn't exist
            CorruptedFileError: If file is corrupted, invalid, or password-protected
        """
        validate_file_exists(filepath)
        
        # Lazy import to avoid forcing dependency
        try:
            import pymupdf
        except ImportError as e:
            raise ImportError(
                "PyMuPDF not installed. "
                "Use: uv run --with pymupdf python your_script.py"
            ) from e
        
        # Open PDF file
        try:
            doc = pymupdf.open(str(filepath))
        except pymupdf.FileDataError as e:
            raise CorruptedFileError(
                f"Invalid PDF structure - file may be corrupted: {e}"
            ) from e
        except Exception as e:
            # Detect password-protected files
            error_msg = str(e).lower()
            if "password" in error_msg or "encrypted" in error_msg:
                raise CorruptedFileError(
                    "Password-protected PDF files are not supported. "
                    "Please provide an unencrypted version."
                ) from e
            # Generic error handling
            raise CorruptedFileError(
                f"Failed to open PDF file: {e}"
            ) from e
        
        try:
            text_parts = []
            
            # Extract text from each page
            for page_num, page in enumerate(doc, start=1):
                # Extract text with natural reading order
                # sort=True ensures left-to-right, top-to-bottom ordering
                page_text = page.get_text("text", sort=True)
                
                # Skip empty pages
                if page_text.strip():
                    text_parts.append(f"\n=== PAGE {page_num} ===\n")
                    text_parts.append(page_text)
            
            return "\n".join(text_parts)
        
        finally:
            # Always close document to free resources
            doc.close()
