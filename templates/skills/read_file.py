#!/usr/bin/env -S uv run --with python-docx --with openpyxl --with PyMuPDF python
"""
Universal File Reader CLI - Auto-detect and extract text from documents

Supports: DOCX, XLSX, PDF (auto-detected by extension)

Usage:
    uv run skills/read_file.py <filepath>
    uv run skills/read_file.py --list-formats
    uv run skills/read_file.py --format pdf <file.txt>
    uv run skills/read_file.py --help
    uv run skills/read_file.py --version

Examples:
    uv run skills/read_file.py report.pdf > report.txt
    uv run skills/read_file.py data.xlsx > data.txt
    uv run skills/read_file.py --list-formats
    uv run skills/read_file.py --format docx corrupted.bin 2>/dev/null

Exit Codes:
    0 - Success (text extracted or --list-formats executed)
    1 - File error (not found, corrupted, unsupported format)
    2 - Unexpected error

Domain: Skills (Infrastructure)
Pattern: CLI Facade (Adapter) + Registry (Auto-discovery)
REQ-011: File Reader Skills System
QUANT-011-005: Universal CLI Implementation
"""
import sys
from pathlib import Path

# Add file_readers module to path
sys.path.insert(0, str(Path(__file__).parent))

from file_readers.base import (AbstractFileReader, FileReaderError,
                               UnsupportedFormatError)


def list_formats() -> None:
    """
    Print all supported file formats to stdout.
    
    Formats are retrieved from the auto-discovery registry and
    displayed in alphabetical order without leading dots.
    """
    formats = AbstractFileReader.list_supported_formats()
    if formats:
        print(f"Supported formats: {', '.join(formats)}")
    else:
        print("No file readers registered")


def main() -> int:
    """Main entry point for Universal File Reader CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Universal file reader with auto-detection (DOCX, XLSX, PDF)",
        epilog="Part of SIA Framework - File Reader Skills System"
    )
    parser.add_argument(
        "filepath",
        nargs="?",
        help="Path to file to read (required unless --list-formats)"
    )
    parser.add_argument(
        "--format",
        help="Force specific format (overrides auto-detection). Example: --format pdf"
    )
    parser.add_argument(
        "--list-formats",
        action="store_true",
        help="List all supported file formats and exit"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="read_file 1.0.0 (SIA Framework)"
    )
    
    args = parser.parse_args()
    
    # Handle --list-formats (no filepath required)
    if args.list_formats:
        list_formats()
        return 0
    
    # Validate filepath is provided for read operations
    if not args.filepath:
        sys.stderr.write("Error: filepath is required (unless --list-formats is used)\n")
        sys.stderr.write("Try 'read_file.py --help' for more information.\n")
        return 1
    
    try:
        filepath = Path(args.filepath)
        
        # Get reader: either forced format or auto-detect
        if args.format:
            # Force specific format by creating a virtual path with the desired extension
            # This allows format override without modifying the actual file
            virtual_path = filepath.with_suffix(f".{args.format}")
            reader = AbstractFileReader.get_reader(virtual_path)
        else:
            # Auto-detect based on file extension
            reader = AbstractFileReader.get_reader(filepath)
        
        # Read the ACTUAL file (not the virtual path used for selection)
        text = reader.read(filepath)
        
        # Output text to stdout
        print(text, end='')
        return 0
        
    except FileNotFoundError as e:
        sys.stderr.write(f"Error: {e}\n")
        return 1
        
    except UnsupportedFormatError as e:
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
