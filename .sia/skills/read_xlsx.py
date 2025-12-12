#!/usr/bin/env -S uv run --with openpyxl python
"""
XLSX File Reader CLI - Extract text from Microsoft Excel spreadsheets

Usage:
    uv run skills/read_xlsx.py <file.xlsx>
    uv run skills/read_xlsx.py --help
    uv run skills/read_xlsx.py --version

Examples:
    uv run skills/read_xlsx.py data.xlsx > data.txt
    uv run skills/read_xlsx.py spreadsheet.xlsx 2>/dev/null

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
from file_readers.xlsx_reader import XlsxReader


def main() -> int:
    """Main entry point for XLSX CLI facade"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract text from XLSX files (Microsoft Excel)",
        epilog="Part of SIA Framework - File Reader Skills System"
    )
    parser.add_argument(
        "filepath",
        help="Path to XLSX file to read"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="read_xlsx 1.0.0 (SIA Framework)"
    )
    
    args = parser.parse_args()
    
    try:
        filepath = Path(args.filepath)
        reader = XlsxReader()
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
