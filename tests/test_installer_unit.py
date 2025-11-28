#!/usr/bin/env python3
"""
Unit tests for SIA installer modules (direct imports)
Tests actual code coverage without subprocess isolation
"""

import sys
import tempfile
from pathlib import Path

import pytest

# Add installer to path
sys.path.insert(0, str(Path(__file__).parent.parent / "installer"))

from install import SIAInstaller


class TestSIAInstallerUnit:
    """Unit tests for SIAInstaller class methods"""
    
    def test_installer_initialization(self):
        """Test that SIAInstaller initializes with correct paths"""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                installer = SIAInstaller()
                
                assert installer.platform in ["Linux", "Darwin", "Windows"]
                # Use resolve() to handle symlinks like /var -> /private/var on macOS
                assert installer.root.resolve() == Path(tmpdir).resolve()
                assert installer.sia_dir.resolve() == (Path(tmpdir) / ".sia").resolve()
                assert installer.vscode_dir.resolve() == (Path(tmpdir) / ".vscode").resolve()
            finally:
                os.chdir(old_cwd)
                
    def test_command_exists_detection(self):
        """Test that _command_exists detects available commands"""
        installer = SIAInstaller()
        
        # Python should always exist (we're running in it)
        assert installer._command_exists("python3") or installer._command_exists("python")
        
        # Non-existent command
        assert not installer._command_exists("this_command_definitely_does_not_exist_12345")
        
        # uv should exist (auto-installed by framework)
        # Note: This may fail on fresh systems, which is expected behavior
        # The installer will auto-install uv in that case
    
    def test_install_uv_method_exists(self):
        """Test that _install_uv method is available"""
        installer = SIAInstaller()
        
        # Verify method exists
        assert hasattr(installer, '_install_uv')
        assert callable(getattr(installer, '_install_uv'))
        
    def test_print_header_output(self, capsys):
        """Test that _print_header produces expected output"""
        installer = SIAInstaller()
        installer._print_header()
        
        captured = capsys.readouterr()
        assert "SIA Framework Installer" in captured.out
        assert installer.platform in captured.out
        
    def test_readme_content_generation(self):
        """Test that README content is well-formed"""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                
                # Create minimal sia/ structure
                sia_dir = Path(tmpdir) / "sia" / "templates"
                sia_dir.mkdir(parents=True)
                
                # Create template files
                (sia_dir / "INIT_REQUIRED.template.md").write_text("# Init template")
                (sia_dir / "gitignore.template").write_text("# Gitignore template\n__pycache__/")
                (sia_dir / "vscode-settings.template.json").write_text('{"locale": "{{LOCALE}}"}')
                
                prompts_dir = sia_dir / "prompts"
                prompts_dir.mkdir()
                (prompts_dir / "test.prompt.md").write_text("# Test prompt")
                
                installer = SIAInstaller()
                installer._create_structure()
                
                # Verify README files created
                assert (Path(tmpdir) / ".sia" / "README.md").exists()
                assert (Path(tmpdir) / ".sia" / "agents" / "README.md").exists()
                
                # Verify content
                main_readme = (Path(tmpdir) / ".sia" / "README.md").read_text()
                assert "SIA Project Configuration" in main_readme
                assert "Structure" in main_readme
                
            finally:
                os.chdir(old_cwd)
                

class TestAutoDiscoveryUnit:
    """Unit tests for auto_discovery.py module"""
    
    @pytest.fixture
    def mock_project(self):
        """Create a mock project structure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "mock_project"
            project_dir.mkdir()
            
            # Create Python files
            (project_dir / "main.py").write_text("# Main file")
            (project_dir / "requirements.txt").write_text("fastapi==0.100.0\n")
            
            # Create domain structure
            domain_dir = project_dir / "domain"
            domain_dir.mkdir()
            (domain_dir / "__init__.py").write_text("")
            (domain_dir / "users").mkdir()
            (domain_dir / "users" / "__init__.py").write_text("")
            
            yield project_dir
    
    def test_project_detection(self, mock_project):
        """Test that auto_discovery detects project structure"""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "installer"))
        
        # Import requires pyyaml - skip if not available
        try:
            import yaml
        except ImportError:
            pytest.skip("pyyaml not installed - use: uv pip install pyyaml")
        
        from auto_discovery import ProjectDiscovery
        
        discovery = ProjectDiscovery(mock_project)
        result = discovery.discover()
        
        assert result is not None
        assert "project" in result
        assert result["project"]["type"] in ["python", "fastapi", "generic"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=installer", "--cov-report=term", "--cov-report=html:htmlcov_unit"])
