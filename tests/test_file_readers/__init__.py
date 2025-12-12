"""
Test configuration and fixtures for file_readers tests.

Provides shared fixtures and utilities for testing file readers.
"""

import sys
from pathlib import Path

import pytest

# Add templates/skills to Python path for imports
skills_path = Path(__file__).parent.parent.parent / "templates" / "skills"
sys.path.insert(0, str(skills_path))
