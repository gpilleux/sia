#!/usr/bin/env python3
"""
SIA Installer Test Suite
Tests installation in isolated temporary directories without affecting local installation
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


class TestSIAInstaller:
    """Test suite for SIA installer scripts"""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory with SIA framework"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            project_dir.mkdir()
            
            # Copy SIA framework to temp directory
            sia_src = Path(__file__).parent.parent  # Root of SIA repo
            sia_dest = project_dir / "sia"
            shutil.copytree(sia_src, sia_dest, 
                          ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc', '.sia', '.vscode'))
            
            yield project_dir
            
    def test_install_py_creates_structure(self, temp_project):
        """Test that install.py creates all required directories"""
        # Run installer
        result = subprocess.run(
            ["python3", "sia/installer/install.py"],
            cwd=temp_project,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Installer failed: {result.stderr}"
        
        # Verify directory structure
        expected_dirs = [
            ".sia",
            ".sia/agents",
            ".sia/knowledge/active",
            ".sia/knowledge/_archive",
            ".sia/requirements",
            ".sia/requirements/_archive",
            ".sia/skills",
            ".sia/prompts",
            ".vscode",
            ".github",
        ]
        
        for expected_dir in expected_dirs:
            dir_path = temp_project / expected_dir
            assert dir_path.exists(), f"Directory {expected_dir} not created"
            assert dir_path.is_dir(), f"{expected_dir} is not a directory"
            
    def test_install_py_creates_readme_files(self, temp_project):
        """Test that install.py creates all README files"""
        # Run installer
        subprocess.run(
            ["python3", "sia/installer/install.py"],
            cwd=temp_project,
            capture_output=True
        )
        
        # Verify README files
        expected_readmes = [
            ".sia/README.md",
            ".sia/agents/README.md",
            ".sia/knowledge/active/README.md",
            ".sia/requirements/README.md",
            ".sia/skills/README.md",
        ]
        
        for readme in expected_readmes:
            readme_path = temp_project / readme
            assert readme_path.exists(), f"README {readme} not created"
            assert readme_path.read_text().strip(), f"README {readme} is empty"
            
    def test_install_py_creates_config_files(self, temp_project):
        """Test that install.py creates configuration files"""
        # Run installer
        subprocess.run(
            ["python3", "sia/installer/install.py"],
            cwd=temp_project,
            capture_output=True
        )
        
        # Verify configuration files
        expected_configs = [
            ".sia.detected.yaml",
            ".sia/INIT_REQUIRED.md",
            ".vscode/settings.json",
            ".github/copilot-instructions.md",
        ]
        
        for config in expected_configs:
            config_path = temp_project / config
            assert config_path.exists(), f"Config {config} not created"
            
    def test_install_py_installs_slash_commands(self, temp_project):
        """Test that install.py copies all slash command prompts"""
        # Run installer
        subprocess.run(
            ["python3", "sia/installer/install.py"],
            cwd=temp_project,
            capture_output=True
        )
        
        # Verify prompts directory
        prompts_dir = temp_project / ".sia/prompts"
        assert prompts_dir.exists(), "Prompts directory not created"
        
        # Count prompt files
        prompt_files = list(prompts_dir.glob("*.prompt.md"))
        assert len(prompt_files) >= 10, f"Expected at least 10 prompts, found {len(prompt_files)}"
        
        # Verify specific prompts exist
        critical_prompts = ["activate.prompt.md", "boost.prompt.md", "quant.prompt.md"]
        for prompt in critical_prompts:
            prompt_path = prompts_dir / prompt
            assert prompt_path.exists(), f"Critical prompt {prompt} not found"
            
    def test_install_py_creates_gitignore(self, temp_project):
        """Test that install.py creates .gitignore from template"""
        # Run installer
        subprocess.run(
            ["python3", "sia/installer/install.py"],
            cwd=temp_project,
            capture_output=True
        )
        
        gitignore = temp_project / ".gitignore"
        assert gitignore.exists(), ".gitignore not created"
        
        content = gitignore.read_text()
        # Check for SIA framework marker
        assert "SIA Framework" in content or "__pycache__" in content, ".gitignore not from template"
        
    def test_install_py_respects_existing_files(self, temp_project):
        """Test that install.py doesn't overwrite existing configuration"""
        # Create existing files
        vscode_dir = temp_project / ".vscode"
        vscode_dir.mkdir(parents=True, exist_ok=True)
        existing_settings = vscode_dir / "settings.json"
        existing_settings.write_text('{"custom": "setting"}')
        
        gitignore = temp_project / ".gitignore"
        gitignore.write_text("# Custom gitignore\n*.log")
        
        # Run installer
        result = subprocess.run(
            ["python3", "sia/installer/install.py"],
            cwd=temp_project,
            capture_output=True,
            text=True
        )
        
        # Verify existing files preserved
        assert existing_settings.read_text() == '{"custom": "setting"}', "Existing settings.json overwritten"
        assert "Custom gitignore" in gitignore.read_text(), "Existing .gitignore overwritten"
        
        # Verify warning messages
        assert "already exists" in result.stdout, "No warning about existing files"
        
    def test_install_py_auto_discovery_runs(self, temp_project):
        """Test that install.py triggers auto-discovery"""
        # Run installer
        subprocess.run(
            ["python3", "sia/installer/install.py"],
            cwd=temp_project,
            capture_output=True
        )
        
        # Verify auto-discovery output
        detected_yaml = temp_project / ".sia.detected.yaml"
        assert detected_yaml.exists(), "Auto-discovery didn't generate .sia.detected.yaml"
        
        content = detected_yaml.read_text()
        # YAML format uses nested structure: project.name (not project_name)
        assert "project:" in content and "name:" in content, "Invalid .sia.detected.yaml format"
        
    def test_install_sh_parity(self, temp_project):
        """Test that install.sh produces identical structure to install.py"""
        # Run install.sh
        result = subprocess.run(
            ["bash", "sia/installer/install.sh"],
            cwd=temp_project,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"install.sh failed: {result.stderr}"
        
        # Verify critical files exist (same as install.py)
        critical_paths = [
            ".sia/agents",
            ".sia/prompts",
            ".vscode/settings.json",
            ".github/copilot-instructions.md",
            ".sia.detected.yaml",
        ]
        
        for path in critical_paths:
            full_path = temp_project / path
            assert full_path.exists(), f"install.sh didn't create {path}"
            
    @pytest.mark.parametrize("installer", ["install.py", "install.sh"])
    def test_installer_idempotency(self, temp_project, installer):
        """Test that running installer twice is safe"""
        cmd = ["python3" if installer.endswith(".py") else "bash", f"sia/installer/{installer}"]
        
        # Run installer first time
        result1 = subprocess.run(cmd, cwd=temp_project, capture_output=True)
        assert result1.returncode == 0, f"First run failed: {result1.stderr}"
        
        # Run installer second time
        result2 = subprocess.run(cmd, cwd=temp_project, capture_output=True)
        assert result2.returncode == 0, f"Second run failed: {result2.stderr}"
        
        # Verify no corruption
        assert (temp_project / ".sia/agents").exists(), "Structure corrupted on second run"
        
    def test_python_version_check(self, temp_project):
        """Test that installer validates Python version"""
        # This test assumes Python 3.10+ is installed
        result = subprocess.run(
            ["python3", "sia/installer/install.py"],
            cwd=temp_project,
            capture_output=True,
            text=True
        )
        
        # Should succeed with valid Python
        assert result.returncode == 0, "Installer failed with valid Python version"
        
        # Check version detection in output
        assert "Python" in result.stdout, "No Python version info in output"


class TestSmartInit:
    """Test suite for smart_init.py"""
    
    @pytest.fixture
    def temp_project_with_sia(self):
        """Create temp project with SIA framework"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            project_dir.mkdir()
            
            sia_src = Path(__file__).parent.parent
            sia_dest = project_dir / "sia"
            shutil.copytree(sia_src, sia_dest,
                          ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc', '.sia'))
            
            # Create minimal .sia structure
            (project_dir / ".sia/agents").mkdir(parents=True)
            (project_dir / ".sia/requirements").mkdir(parents=True)
            (project_dir / ".sia/skills").mkdir(parents=True)
            
            yield project_dir
            
    def test_smart_init_generates_yaml(self, temp_project_with_sia):
        """Test that smart_init.py generates .sia.detected.yaml"""
        result = subprocess.run(
            ["uv", "run", "--with", "pyyaml", "python3", "sia/installer/smart_init.py"],
            cwd=temp_project_with_sia,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(temp_project_with_sia / "sia")}
        )
        
        assert result.returncode == 0, f"smart_init.py failed: {result.stderr}"
        
        yaml_file = temp_project_with_sia / ".sia.detected.yaml"
        assert yaml_file.exists(), ".sia.detected.yaml not generated"
        
        content = yaml_file.read_text()
        # YAML format uses nested structure: project.name (not project_name)
        assert "project:" in content and "name:" in content, "Invalid .sia.detected.yaml format"


class TestDockerIntegration:
    """Test installer in Docker containers for true cross-platform validation"""
    
    @pytest.mark.skip(reason="Requires Docker, run manually with: pytest -v -m docker")
    @pytest.mark.docker
    def test_install_in_ubuntu_container(self):
        """Test installation in Ubuntu Docker container"""
        dockerfile_content = """
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3 python3-pip git
WORKDIR /workspace
COPY . /workspace/sia
RUN python3 sia/installer/install.py
"""
        # Implementation requires docker-py library
        # This is a placeholder for future implementation
        pass
    
    @pytest.mark.skip(reason="Requires Docker, run manually")
    @pytest.mark.docker
    def test_install_in_alpine_container(self):
        """Test installation in Alpine Linux container"""
        # Lightweight Linux distro test
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
