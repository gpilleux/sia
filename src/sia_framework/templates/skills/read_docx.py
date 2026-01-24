#!/usr/bin/env -S uv run --with python-docx python
"""
DOCX File Reader CLI - Extract text from Microsoft Word documents

Usage:
    uv run skills/read_docx.py <file.docx>
    uv run skills/read_docx.py --help
    uv run skills/read_docx.py --version

Examples:
    uv run skills/read_docx.py report.docx > report.txt
    uv run skills/read_docx.py document.docx 2>/dev/null

Exit Codes:
    0 - Success (text extracted)
    1 - File error (not found, corrupted, password-protected)
    2 - Unexpected error

Domain: Skills (Infrastructure)
Pattern: CLI Facade (Adapter)
REQ-011: File Reader Skills System
QUANT-011-004: CLI Facades Implementation
"""
import sys
from pathlib import Path

# Add file_readers module to path
sys.path.insert(0, str(Path(__file__).parent))

from file_readers.base import FileReaderError
from file_readers.docx_reader import DocxReader


def main() -> int:
    """Main entry point for DOCX CLI facade"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract text from DOCX files (Microsoft Word)",
        epilog="Part of SIA Framework - File Reader Skills System"
    )
    parser.add_argument(
        "filepath",
        help="Path to DOCX file to read"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="read_docx 1.0.0 (SIA Framework)"
    )
    
    args = parser.parse_args()
    
    try:
        filepath = Path(args.filepath)
        reader = DocxReader()
        text = reader.read(filepath)
        
        # Output text to stdout
        print(text, end='')
        return 0
        
    except FileNotFoundError as e:
        sys.stderr.write(f"Error: {e}\n")
        return 1
        
    except FileReaderError as e:
        # Catches CorruptedFileError and other reader-specific errors
        sys.stderr.write(f"Error: {e}\n")
        return 1
        
    except Exception as e:
        # Unexpected errors (programming bugs, system issues)
        sys.stderr.write(f"Unexpected error: {type(e).__name__}: {e}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
